---
title: "Atlassian Data Center Ends in 2029: Writing Scripts That Run on Both Data Center and Cloud"
summary: |
  Jira and Confluence Data Center reach end of life on March 28, 2029. Until then many teams run both, and automation scripts written for Data Center fail on Cloud. This post lists the differences that affect a script: authentication, user identifiers, Jira search, project listing, the Confluence v2 API and pagination. Then it shows one code path that works on both, first by hand with requests, then with atlassian-api-py 2.0, which I maintain.
tags:
  - Jira
  - Python
  - DevOps
authors:
  - shenxianpeng
date: 2026-11-15
draft: true
---

In October 2026 I added Atlassian Cloud support to [atlassian-api-py][aap], a library I maintain. Counting in the current source, the methods that need separate handling on Data Center and Cloud are 8 of the 40 in the Jira client and 18 of the 23 in the Confluence client.

Once the data has moved to Cloud, scripts written for Data Center start returning 401 and 410.

This post lists the differences that affect a script, then shows a way to write one that runs on both. The first half uses plain `requests`; you don't need my library for it.

## The timeline

From [Atlassian's announcement][eol]:

| Date | What happens |
|---|---|
| 2026-03-30 | New customers can no longer buy Data Center subscriptions |
| 2028-03-30 | Existing customers can no longer buy new subscriptions or expansions |
| 2029-03-28 | End of life: subscriptions expire and the products become read-only |

This applies to Jira Software, Jira Service Management, Confluence and Crowd. Bitbucket and Bamboo Data Center are not included, which I covered in [another post][prev-post].

2029 is more than two years away. In the meantime many teams will have some projects on Cloud and some still on Data Center. Their scripts either exist twice or work on both.

## Authentication

| | Data Center | Cloud |
|---|---|---|
| Recommended | Personal access token, `Authorization: Bearer <token>` | Account email plus API token, basic auth |
| Username and password | Works with basic auth | Deprecated |

Data Center has supported [personal access tokens][pat] since Jira 8.14 and Confluence 7.9. The token goes in a Bearer header, with no username.

A Cloud [API token][basic-auth] is sent together with the account email as basic auth. The documentation does not describe a Bearer form. Put a Cloud API token in a Bearer header, as you would on Data Center, and authentication fails with 401.

## Users: username becomes accountId

The Cloud REST API has no `username` or `userKey`. A user is identified by `accountId` only, a change that [took effect in 2019][gdpr]. Every place that passes a user has to change:

| Operation | Data Center | Cloud |
|---|---|---|
| Assign an issue | `{"name": "jdoe"}` | `{"accountId": "5b10ac8d82e05b22cc7d4ef5"}` |
| Get a user | `GET /user?username=jdoe` | `GET /user?accountId=...` |
| Find users | `GET /user/search?username=jo` | `GET /user/search?query=jo` |
| Add a watcher | The body is a username | The body is an accountId |
| JQL | `assignee = jdoe` | `assignee = 5b10ac8d82e05b22cc7d4ef5` |

The user objects in responses change too: on Cloud they have no `name` or `key`.

Usernames hard-coded in a script, and a "default assignee" in a config file, all have to become accountIds. You can look them up with `/user/search?query=`, which matches the start of a display name or email address. What comes back depends on each user's privacy settings, so a user who hides their email address is returned without it.

`currentUser()` in JQL works on both and can stay.

## Jira search

On Cloud, `/rest/api/2/search` returns 410 and you have to call `/rest/api/2/search/jql`: paging moves from `startAt` to `nextPageToken`, the response has no `total`, only `id` is returned by default, and the JQL must be bounded.

The details and the usual mistakes are in a separate post: [Jira Cloud /rest/api/2/search returns 410 Gone][search-post].

## Other Jira differences

- **Listing projects.** On Data Center, `GET /rest/api/2/project` returns every project in one response. On Cloud that endpoint is [marked as deprecated][project-docs], and its replacement `/rest/api/2/project/search` is paginated: at most 100 per page, `startAt` to move on, `isLast` to know when to stop.
- **Creating a version.** Data Center takes the project key (`"project": "OPS"`). On Cloud `project` is deprecated and you send the numeric `projectId`.
- **Changelog.** On Cloud, `expand=changelog` returns only recent entries. For the full history, page through `GET /rest/api/2/issue/{key}/changelog`.
- **Rich text fields.** In the Cloud v3 API, `description` and comment bodies are Atlassian Document Format. Stay on `/rest/api/2/` and both deployments give you strings.

## Confluence: the v1 content endpoints are gone

Confluence differs the most. On Cloud every path sits under `/wiki`, and the v1 content endpoints were [removed on May 1, 2025][change-2520]; calling them returns 410. The removed list includes:

- Reading, creating, updating and deleting content: `/rest/api/content`, `/rest/api/content/{id}`
- Page history, child pages, comments, labels and the attachment list
- Spaces: `/rest/api/space`, `/rest/api/space/{key}`

The replacement is the [REST API v2][confluence-v2] under `/wiki/api/v2`. More than the path changed:

| | Data Center (v1) | Cloud (v2) |
|---|---|---|
| Pages and blog posts | One `/content`, told apart by `type` | Separate `/pages` and `/blogposts` |
| Spaces | By key, such as `DOCS` | By numeric ID; get it with `GET /spaces?keys=DOCS` |
| A page's space | `space.key` | `spaceId` |
| Parent page | `ancestors: [{"id": ...}]` | `parentId` |
| Body | `expand=body.storage` | `body-format=storage` |
| Paging | `start` and `limit` | `cursor`; `limit` is at most 250 |

Two defaults differ as well. A v2 page list includes archived pages unless you add `status=current`. And a page created in v2 without a `parentId` only lands at the root of the space if you add `root-level=true`.

CQL search, `/rest/api/content/search`, is not on the removed list and still works on Cloud.

## Pagination at a glance

| Endpoint | Data Center | Cloud |
|---|---|---|
| Jira search | `startAt`, compare with `total` | `nextPageToken`, stop when there is none |
| Jira project list | Not paginated | `startAt`, check `isLast` |
| Confluence lists | `start`, check `_links.next` | `cursor`, check `_links.next` |

Confluence has one thing in common on both sides: if the response has `_links.next`, there is another page, and if it doesn't, you are done. What differs is whether that link carries `start` or `cursor`.

## A small adapter by hand

The list of differences is long, but a given script usually touches only a few of them. What I do is keep "which one am I talking to" in one place and let the rest of the code look at a single boolean.

The connection comes first. Cloud sites live under `*.atlassian.net`, and that is what this code checks. For a site on a custom domain you can call `GET /rest/api/2/serverInfo` instead; on Cloud its `deploymentType` is always `Cloud`.

```python
from urllib.parse import parse_qs, urlsplit

import requests


class Atlassian:
    def __init__(self, url, *, user=None, secret):
        self.url = url.rstrip("/")
        self.cloud = (urlsplit(self.url).hostname or "").endswith(".atlassian.net")
        self.http = requests.Session()
        if self.cloud:
            self.http.auth = (user, secret)  # account email + API token
        else:
            self.http.headers["Authorization"] = f"Bearer {secret}"  # PAT

    def call(self, method, path, **kwargs):
        r = self.http.request(method, self.url + path, timeout=60, **kwargs)
        r.raise_for_status()
        return r.json() if r.content else None
```

Then each operation that differs gets one function, and the branch stays inside it:

```python
def search(jira, jql, fields):
    payload = {"jql": jql, "maxResults": 100, "fields": fields}
    if jira.cloud:
        while True:
            page = jira.call("POST", "/rest/api/2/search/jql", json=payload)
            yield from page.get("issues", [])
            if not page.get("nextPageToken"):
                return
            payload["nextPageToken"] = page["nextPageToken"]
    payload["startAt"] = 0
    while True:
        page = jira.call("POST", "/rest/api/2/search", json=payload)
        yield from page["issues"]
        payload["startAt"] += len(page["issues"])
        if not page["issues"] or payload["startAt"] >= page["total"]:
            return


def assign(jira, issue_key, user):
    # user: accountId on Cloud, username on Data Center
    field = "accountId" if jira.cloud else "name"
    jira.call("PUT", f"/rest/api/2/issue/{issue_key}/assignee", json={field: user})


def pages_in_space(wiki, space_key):
    if wiki.cloud:
        spaces = wiki.call("GET", "/api/v2/spaces", params={"keys": space_key})
        space_id = spaces["results"][0]["id"]
        path = f"/api/v2/spaces/{space_id}/pages"
        params = {"status": "current", "limit": 100}
    else:
        path = "/rest/api/content"
        params = {"spaceKey": space_key, "type": "page", "limit": 100}
    while True:
        page = wiki.call("GET", path, params=params)
        yield from page["results"]
        next_link = page.get("_links", {}).get("next")
        if not next_link:
            return
        key = "cursor" if wiki.cloud else "start"
        params[key] = parse_qs(urlsplit(next_link).query)[key][0]
```

The code that does the actual work no longer cares which side it is on:

```python
jira = Atlassian(
    "https://your-site.atlassian.net",
    user="you@example.com",
    secret="your-api-token",
)
# jira = Atlassian("https://jira.company.com", secret="your-personal-access-token")

for issue in search(jira, "project = OPS AND status = Open", ["summary", "assignee"]):
    print(issue["key"], issue["fields"]["summary"])

wiki = Atlassian(
    "https://your-site.atlassian.net/wiki",
    user="you@example.com",
    secret="your-api-token",
)
# wiki = Atlassian("https://confluence.company.com", secret="your-personal-access-token")

for page in pages_in_space(wiki, "DOCS"):
    print(page["id"], page["title"])
```

This has two advantages. The branches sit in a handful of functions, so when the migration is over you delete the Data Center half. And it is easy to test: run the same function against two sets of mocks.

What it cannot hide is the data. The second argument of `assign()` is a username on one side and an accountId on the other. A page from `pages_in_space()` has `space` on one side and `spaceId` on the other. The function names are the same; what goes in and what comes out are still two different things.

## The same with atlassian-api-py

[atlassian-api-py][aap] 2.0 has this adapter built in. The Jira and Confluence clients detect Cloud from the URL and keep one set of method names and arguments.

```sh
pip install atlassian-api-py
```

The example below needs version 2.0 or later.

```python
import os

from atlassian_api import Confluence, Jira

credentials = {
    "username": os.environ.get("ATLASSIAN_USER"),  # Cloud: account email
    "password": os.environ.get("ATLASSIAN_API_TOKEN"),  # Cloud: API token
    "token": os.environ.get("ATLASSIAN_PAT"),  # Data Center: personal access token
}
jira = Jira(url=os.environ["JIRA_URL"], **credentials)
confluence = Confluence(url=os.environ["CONFLUENCE_URL"], **credentials)

for issue in jira.iter_issues(
    "project = OPS AND status = Open", fields=["summary", "assignee"]
):
    print(issue["key"], issue["fields"]["summary"])

print(jira.count_issues("project = OPS AND status = Open"))

# username on Data Center, accountId on Cloud
jira.assign_issue("OPS-1", os.environ["DEFAULT_ASSIGNEE"])

print([project.key for project in jira.get_projects()])

for page in confluence.get_content_by_space("DOCS", limit=50).results:
    print(page.id, page.title)

confluence.create_or_update_page("DOCS", "Nightly report", "<p>All green</p>")
```

The code is the same for Cloud and Data Center; only the environment differs. For Cloud, set `ATLASSIAN_USER` and `ATLASSIAN_API_TOKEN`. For Data Center, set `ATLASSIAN_PAT`. You don't add `/wiki` to a Confluence Cloud URL yourself.

Behind those calls the library does what the earlier sections describe:

- `iter_issues()` and `count_issues()` use `/search/jql` and `/search/approximate-count` on Cloud.
- `assign_issue()` sends `accountId` on Cloud. To find an accountId, call `jira.search_users("jane@example.com")`.
- If you pass `token=` on Cloud by mistake, the 401 error tells you to use the email and API token instead.
- `get_projects()` collects every page of `/project/search` on Cloud and still returns one list.
- The Confluence page, space, child page, comment and label methods use v2 on Cloud, and the library turns the space key into an ID for you. List methods keep the v1 envelope (`results`, `start`, `limit`, `size`), and `start` and `limit` are mapped onto cursors on Cloud. As on Data Center, one call returns at most `limit` items, so for a space with many pages you move `start` forward yourself.

If the site uses a custom domain and the library cannot tell from the URL, pass `cloud=True`.

## What it does not do

It is a small library, so the limits belong up front:

- **The Bitbucket client is for Server and Data Center only.** A `bitbucket.org` URL raises `ValueError`. Bitbucket Data Center is not part of this end of life anyway.
- **There are no Jira Software boards or sprints, and no Jira Service Management API.** If you need those, [atlassian-python-api][apa] covers far more.
- **Returned objects have a different shape on each side.** The library unifies method names, arguments and the list envelope. The objects inside are what each API returns. A Confluence page on Cloud has `spaceId` and no `space.key`; a Jira user on Cloud has `accountId` and no `name`. Code that reads those fields still has to handle both.
- **User identifiers are not converted.** Pass a username to `assign_issue()` on Cloud and the call fails. The library does not look up the accountId for you.
- **`export_page_pdf()` is Data Center only.** On Cloud it raises `NotImplementedError`.
- **The Cloud code paths have been tested against Atlassian's OpenAPI specifications and mocked servers so far.** A nightly test against a live Cloud site is being set up.

All the Python code in this post, the hand-written adapter and the library example, was run against both a Data Center and a Cloud mocked with `responses`. The mocks follow Atlassian's documentation and may differ from a real site.

If a script of yours broke in the migration in a way this post does not mention, leave a comment or [open an issue][issues]. I would like to add it.

[aap]: https://github.com/shenxianpeng/atlassian-api-py
[eol]: https://www.atlassian.com/licensing/data-center-end-of-life
[prev-post]: /posts/2026/jira-cloud-jenkins-bitbucket/
[pat]: https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html
[basic-auth]: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
[gdpr]: https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/
[search-post]: /posts/2026/jira-cloud-search-410/
[project-docs]: https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-projects/#api-rest-api-2-project-get
[change-2520]: https://developer.atlassian.com/changelog/#CHANGE-2520
[confluence-v2]: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
[apa]: https://github.com/atlassian-api/atlassian-python-api
[issues]: https://github.com/shenxianpeng/atlassian-api-py/issues
