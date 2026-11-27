---
title: "Jira Cloud /rest/api/2/search Returns 410 Gone: What Changed and How to Fix Your Script"
summary: |
  Jira Cloud removed /rest/api/2/search and /rest/api/3/search. Calls now fail with 410 Gone and "The requested API has been removed. Please migrate to the /rest/api/3/search/jql API". This post covers what changed, a working pagination loop and issue count with plain requests, the mistakes people make after switching, and why Data Center scripts should stay as they are. The last section does the same with atlassian-api-py 2.0, which I maintain.
tags:
  - Jira
  - Python
  - Troubleshooting
authors:
  - shenxianpeng
date: 2026-11-15
draft: true
---

If a script of yours queries Jira Cloud and has started failing with this, the script is probably fine:

```text
requests.exceptions.HTTPError: 410 Client Error: Gone for url: https://your-site.atlassian.net/rest/api/2/search?jql=project+%3D+TEST&startAt=0&maxResults=100
```

Print the response body and you get this (as posted by a user in [pycontribs/jira#2369][pyjira-issue]):

```json
{
  "errorMessages": [
    "The requested API has been removed. Please migrate to the /rest/api/3/search/jql API. A full migration guideline is available at https://developer.atlassian.com/changelog/#CHANGE-2046"
  ],
  "errors": {}
}
```

Atlassian removed this endpoint from Jira Cloud. Your script did nothing wrong. Below is why it went away, how to change the script, and the mistakes that tend to follow.

A disclosure first: the last section mentions atlassian-api-py, a library I maintain. Its 1.x `search_issue_with_jql()` called this same endpoint and gets the same 410 on Cloud. Everything before that section uses plain `requests`, so you can fix your script without installing anything.

## What happened

| Date | Event |
|---|---|
| 2024-10-31 | Atlassian publishes the deprecation notice [CHANGE-2046][change-2046], with removal planned after May 1, 2025 |
| 2025-06-30 | [CHANGE-2598][change-2598] announces that the endpoints "are now being removed" |
| 2025-09 | Reports of 410 errors appear on GitHub and the Atlassian Community, for example [pycontribs/jira#2369][pyjira-issue] on September 2 |

Four endpoints were removed, all of them on Cloud only:

- `GET /rest/api/2|3|latest/search`
- `POST /rest/api/2|3|latest/search`
- `POST /rest/api/2|3|latest/search/id`
- `POST /rest/api/2|3|latest/expression/eval`

The reason Atlassian gives in the notice is that the old endpoints expose parameters that are not compatible with its new JQL service. The replacement is `GET` and `POST /rest/api/3/search/jql`, which Atlassian calls enhanced search.

## Old endpoint versus new endpoint

This table comes from CHANGE-2046 and Atlassian's [API reference][search-docs].

| | Old `/search` | New `/search/jql` |
|---|---|---|
| Paging | `startAt`, with `total` in the response | `nextPageToken`; the last page has no token and `isLast` is `true` |
| Total count | `total` in the response | Gone. Call `POST /search/approximate-count` instead |
| Fields returned by default | `*navigable` | `id` only |
| JQL | Can have no restriction at all | Must be a bounded query, otherwise 400 |
| `validateQuery` | Supported | Removed. Use `/jql/parse` to validate JQL |
| Page size | 50 by default | 50 by default; up to 5000 when you ask for `id` or `key` only, and Jira returns fewer when you ask for many fields |
| Search right after a write | Finds the change | May take a few seconds |

The error message tells you to move to `/rest/api/3/search/jql`. Atlassian's [v2 reference][search-docs-v2] also lists `/rest/api/2/search/jql`.

The two versions differ in what they return. According to the [REST API introduction][v3-intro], version 3 returns an issue's `description`, `environment`, comment bodies and multi-line text custom fields in Atlassian Document Format, which is a nested JSON object. Version 2 returns them as strings.

If your script called `/rest/api/2/search`, change it to `/rest/api/2/search/jql`. Jump to version 3 and every line that treats `description` as a string will break next.

## Before and after

Before, most scripts look like this:

```python
import requests

BASE = "https://your-site.atlassian.net"
AUTH = ("you@example.com", "your-api-token")


def search_all(jql):
    issues, start_at = [], 0
    while True:
        r = requests.get(
            f"{BASE}/rest/api/2/search",
            params={"jql": jql, "startAt": start_at, "maxResults": 100},
            auth=AUTH,
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        issues += data["issues"]
        start_at += len(data["issues"])
        if start_at >= data["total"]:
            return issues
```

After:

```python
def search_all(jql, fields=("summary", "status", "assignee")):
    payload = {"jql": jql, "maxResults": 100, "fields": list(fields)}
    issues = []
    while True:
        r = requests.post(
            f"{BASE}/rest/api/2/search/jql", json=payload, auth=AUTH, timeout=60
        )
        r.raise_for_status()
        data = r.json()
        issues += data.get("issues", [])
        token = data.get("nextPageToken")
        if not token:
            return issues
        payload["nextPageToken"] = token
```

Three things changed:

1. The path gained `/jql`.
2. `fields` is spelled out. Without it you get `id` and nothing else.
3. The loop follows `nextPageToken` and stops when the response has none.

Authentication is the same as before: basic auth with your account email and an [API token][api-token].

## How to get a total count

The new response has no `total`. To find out how many issues match, call a separate endpoint:

```python
def count(jql):
    r = requests.post(
        f"{BASE}/rest/api/2/search/approximate-count",
        json={"jql": jql},
        auth=AUTH,
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["count"]
```

The number is an estimate. The reference says recent updates might not be reflected right away. This endpoint needs a bounded JQL query too.

## Mistakes that follow the switch

### Only IDs come back: `KeyError: 'fields'`

Leave out `fields` and each issue contains only its `id`, so `issue["fields"]["summary"]` raises `KeyError`.

For the old default, send `"fields": ["*navigable"]`. For everything, send `["*all"]`. Listing only the fields you use is still the better choice, because fewer fields means more issues per page.

### Still looping on `startAt` and `total`

A script that got a new URL but kept its old loop fails on `data["total"]` with `KeyError: 'total'`.

`startAt` is not a parameter of the new endpoint either. I have not checked on a live site whether it is ignored or rejected. Either way, it will not get you to page two.

### Treating a short page as the last page

Some scripts stop when a page holds fewer issues than `maxResults`. The new endpoint returns short pages on purpose when you ask for many fields, so this check ends the loop early. There is no error; you get fewer results than there are.

Look at `nextPageToken` only. If it is there, continue. If not, you are done.

### JQL with no restriction returns 400

A query that only sorts, such as `order by created desc`, used to work and now returns 400. The reference gives these examples: `order by key desc` is unbounded, `assignee = currentUser() order by key` is bounded.

Adding one condition is enough, for example `project = TEST`.

### No more fetching pages in parallel

You used to be able to read `total`, then start a few threads for `startAt=0`, `100`, `200`. Now the token for the next page is in the previous response, so pages come one after another. A token is valid for 7 days.

Atlassian's [migration article][pitfalls] suggests two steps. Collect the IDs first, without `fields` and 5000 per page; this part has to be sequential. Then send the IDs in batches of 100 to `POST /rest/api/3/issue/bulkfetch`, which you can call in parallel.

### An issue you just created is not found

The new endpoint does not promise that a search sees a write immediately. CHANGE-2046 says most changes are visible within seconds and bulk operations can take longer.

A script that creates an issue and then searches for it to confirm will fail now and then. When you already know the key, `GET /rest/api/2/issue/{key}` is the safer call. If it has to be a search, the new endpoint takes `reconcileIssues`: up to 50 issue IDs for which the results must be current.

### Comments and changelog are cut off

Search results carry at most 20 comments and 40 changelog entries per issue. For the full lists, call `GET /rest/api/2/issue/{key}/comment` and `GET /rest/api/2/issue/{key}/changelog`.

## Data Center: change nothing

The removal applies to Cloud only. The [Jira Data Center 11.0 REST reference][dc-search] still documents `GET` and `POST /rest/api/2/search` with `startAt` and `maxResults`, and it has no `/search/jql`.

Leave a Data Center script as it is. Apply the changes above and it will call an endpoint the Data Center reference does not list.

The harder case is one script that has to run against both Data Center and Cloud, which is common during a migration. I wrote that up separately: [writing scripts that run on both Data Center and Cloud][dc-cloud-post].

## If you use a library

If the script already goes through a Python library, check whether the library has the new endpoint. The method names below are from each library's current source, checked on November 15, 2026.

**[jira][pyjira] (pycontribs, 3.10.5):** `enhanced_search_issues()` and `approximate_issue_count()`. On Cloud, the existing `search_issues()` sends its first page to the new endpoint and raises `JIRAError` when `startAt` is not 0.

**[atlassian-python-api][apa] (5.0.5):** pass `cloud=True` when you create the client, then use `enhanced_jql()`, `enhanced_jql_get_list_of_tickets()` and `approximate_issue_count()`. With `cloud=True`, the existing `jql()` sends its first page to the new endpoint and raises `ValueError` when `start` is not 0.

```python
from atlassian import Jira

jira = Jira(
    url="https://your-site.atlassian.net",
    username="you@example.com",
    password="your-api-token",
    cloud=True,
)
issues = jira.enhanced_jql_get_list_of_tickets("project = TEST", fields=["summary"])
print(jira.approximate_issue_count("project = TEST")["count"])
```

These three atlassian-python-api methods are for Cloud only and raise `ValueError` when called against Data Center. A script that covers both has to decide which one to call.

**[atlassian-api-py][aap] (2.0 or later):** this is the one I maintain. The method names are the same on both deployments, and the library picks the endpoint from the URL.

```sh
pip install atlassian-api-py
```

```python
from atlassian_api import Jira

jira = Jira(
    url="https://your-site.atlassian.net",
    username="you@example.com",
    password="your-api-token",
)

issues = jira.search_issue_with_jql(
    "project = TEST AND status = Open", fields=["summary", "status"]
)

for issue in jira.iter_issues("project = TEST", fields=["summary"]):
    print(issue["key"], issue["fields"]["summary"])

print(jira.count_issues("project = TEST AND status = Open"))
```

With a `*.atlassian.net` URL, these three methods call `/rest/api/2/search/jql` and `/rest/api/2/search/approximate-count`. Give it a Data Center URL and the same three lines call `/rest/api/2/search`:

```python
jira = Jira(url="https://jira.company.com", token="your-personal-access-token")
```

When you do not pass `fields`, it asks Cloud for `*navigable`, which is the Data Center default, so the same code does not get different fields on the two sides.

Some things you should know before you pick it:

- It is a small library. [pypistats][pypistats] shows 3,715 downloads last month, against more than 8 million for atlassian-python-api. It also covers far fewer endpoints.
- Version 2.0 renamed the import package from `atlassian` to `atlassian_api`, so it installs next to atlassian-python-api in the same environment. Coming from 1.x, you have to change your imports.
- The Cloud code paths have been tested against Atlassian's OpenAPI specifications and mocked servers so far. A nightly test against a live Cloud site is being set up.

All the Python code in this post was run against a Jira mocked with `responses`, including the 410, the paging and the last page that has no token. The mock follows Atlassian's documentation and may differ from a real site. If something behaves differently on yours, please [open an issue][issues].

[pyjira-issue]: https://github.com/pycontribs/jira/issues/2369
[change-2046]: https://developer.atlassian.com/changelog/#CHANGE-2046
[change-2598]: https://developer.atlassian.com/changelog/#CHANGE-2598
[search-docs]: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/
[search-docs-v2]: https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-search/
[v3-intro]: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#version
[api-token]: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
[pitfalls]: https://community.atlassian.com/forums/Jira-articles/Avoiding-Pitfalls-A-Guide-to-Smooth-Migration-to-Enhanced-JQL/ba-p/2985433
[dc-search]: https://developer.atlassian.com/server/jira/platform/rest/v11002/api-group-search/
[dc-cloud-post]: /posts/2026/atlassian-dc-cloud-scripts/
[pyjira]: https://github.com/pycontribs/jira
[apa]: https://github.com/atlassian-api/atlassian-python-api
[aap]: https://github.com/shenxianpeng/atlassian-api-py
[pypistats]: https://pypistats.org/packages/atlassian-api-py
[issues]: https://github.com/shenxianpeng/atlassian-api-py/issues
