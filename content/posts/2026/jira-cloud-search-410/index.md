---
title: "Jira Cloud 的 /rest/api/2/search 返回 410 Gone，脚本该怎么改"
summary: |
  Jira Cloud 上的 /rest/api/2/search 和 /rest/api/3/search 已经被移除，调用会得到 410 和一句 "The requested API has been removed. Please migrate to the /rest/api/3/search/jql API"。这篇讲新旧接口差在哪、用 requests 怎么翻页和计数、改完之后常见的几个坑，以及 Data Center 为什么不用动。最后是我维护的 atlassian-api-py 2.0 里对应的写法。
tags:
  - Jira
  - Python
  - Troubleshooting
authors:
  - shenxianpeng
date: 2026-11-15
draft: true
---

如果你有一个查 Jira Cloud 的脚本，一直跑得好好的，某天开始报这个：

```text
requests.exceptions.HTTPError: 410 Client Error: Gone for url: https://your-site.atlassian.net/rest/api/2/search?jql=project+%3D+TEST&startAt=0&maxResults=100
```

把响应体打出来，是这样一段（摘自 [pycontribs/jira#2369][pyjira-issue] 里用户贴的内容）：

```json
{
  "errorMessages": [
    "The requested API has been removed. Please migrate to the /rest/api/3/search/jql API. A full migration guideline is available at https://developer.atlassian.com/changelog/#CHANGE-2046"
  ],
  "errors": {}
}
```

这个接口在 Cloud 上被 Atlassian 删掉了，脚本本身没有写错。下面讲它为什么没了、怎么改、改完之后常见的几个坑。

先说明一下，最后一节里的 atlassian-api-py 是我维护的库。它 1.x 的 `search_issue_with_jql()` 调的也是这个接口，在 Cloud 上同样是 410。前面几节只用 `requests`，不装任何库也能照着改。

## 发生了什么

| 日期 | 事情 |
|---|---|
| 2024-10-31 | Atlassian 发布弃用通知 [CHANGE-2046][change-2046]，原定 2025 年 5 月 1 日之后移除 |
| 2025-06-30 | [CHANGE-2598][change-2598] 宣布这些接口"正在被移除" |
| 2025-09 | GitHub 和 Atlassian 社区里陆续有人报告 410，比如 9 月 2 日的 [pycontribs/jira#2369][pyjira-issue] |

被移除的一共四个，都只涉及 Cloud：

- `GET /rest/api/2|3|latest/search`
- `POST /rest/api/2|3|latest/search`
- `POST /rest/api/2|3|latest/search/id`
- `POST /rest/api/2|3|latest/expression/eval`

Atlassian 在通知里给的理由是，旧接口暴露的一些参数和新的 JQL 服务不兼容。替代品是 `GET` 和 `POST /rest/api/3/search/jql`，Atlassian 叫它 enhanced search。

## 新旧接口差在哪

下面的内容来自 CHANGE-2046 和 Atlassian 的 [API 文档][search-docs]。

| | 旧接口 `/search` | 新接口 `/search/jql` |
|---|---|---|
| 翻页 | `startAt`，响应里有 `total` | `nextPageToken`，最后一页没有这个字段，`isLast` 为 `true` |
| 总数 | 响应里的 `total` | 没有了，要另外调 `POST /search/approximate-count` |
| 默认返回的字段 | `*navigable` | 只有 `id` |
| JQL | 可以不带任何条件 | 必须带限制条件（bounded query），否则返回 400 |
| `validateQuery` | 支持 | 去掉了，要校验 JQL 得调 `/jql/parse` |
| 每页条数 | 默认 50 | 默认 50；只取 `id` 或 `key` 时一页最多 5000，字段多了 Jira 会少给 |
| 写入后立刻搜索 | 能搜到 | 可能要等几秒 |

报错信息让你迁到 `/rest/api/3/search/jql`。Atlassian 的 [v2 文档][search-docs-v2]里其实也有 `/rest/api/2/search/jql`。

这两个版本的差别在返回格式上。按 [REST API 的说明][v3-intro]，v3 里 issue 的 `description`、`environment`、评论正文和多行文本的自定义字段是 Atlassian Document Format，一个嵌套的 JSON 对象，v2 里则是字符串。

脚本原来用 `/rest/api/2/search`，就改成 `/rest/api/2/search/jql`。直接换到 3，后面把 `description` 当字符串处理的代码会跟着出问题。

## 改之前和改之后

改之前，大多数脚本长这样：

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

改之后：

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

改了三处：

1. 路径多了 `/jql`。
2. 明确写上 `fields`，不写就只有 `id`。
3. 循环靠 `nextPageToken` 往下走，响应里没有它就结束。

认证没变，还是账号邮箱加 [API token][api-token] 的 Basic 认证。

## 怎么拿总数

新接口的响应里没有 `total`。想知道一共匹配多少条，要调另一个接口：

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

它返回的是估计值，文档写明刚发生的改动不一定马上算进去。它同样要求 JQL 带限制条件。

## 改完之后常见的几个坑

### 只拿到 id，`KeyError: 'fields'`

不传 `fields`，新接口每个 issue 只返回 `id`，后面的 `issue["fields"]["summary"]` 直接报 `KeyError`。

想要旧接口的默认行为，传 `"fields": ["*navigable"]`；想要全部字段，传 `["*all"]`。最好还是只列用得到的字段，字段越少，一页能拿到的条数越多。

### 还在用 `startAt` 和 `total` 循环

只改了 URL、循环没动的脚本，会在 `data["total"]` 这一行报 `KeyError: 'total'`。

`startAt` 也不在新接口的参数表里。带上它会被忽略还是被拒绝，我没有在真实站点上验证过，不管是哪种，都翻不到下一页。

### 用"这一页没满"判断结束

有些脚本看到返回的条数小于 `maxResults` 就认为到头了。新接口在字段多的时候会主动少给，这个判断会让脚本提前结束，而且不报错，只是结果少了。

只看 `nextPageToken`，有就继续，没有就结束。

### JQL 没有限制条件，返回 400

`order by created desc` 这样只有排序的 JQL，以前能跑，现在返回 400。文档里举的例子是：`order by key desc` 不行，`assignee = currentUser() order by key` 可以。

加一个条件就好，比如 `project = TEST`。

### 不能并发翻页

以前可以先拿 `total`，再开几个线程分别取 `startAt=0`、`100`、`200`。现在下一页的 token 在上一页的响应里，只能一页一页来。token 的有效期是 7 天。

Atlassian 在[这篇迁移说明][pitfalls]里给的办法分两步。先不带 `fields`、一页 5000 条把 `id` 拿全，这一步只能串行。再把 `id` 按 100 个一组交给 `POST /rest/api/3/issue/bulkfetch`，这一步可以并发。

### 刚创建的 issue 搜不到

新接口不保证写入后立刻能搜到。CHANGE-2046 的说法是多数改动几秒内可见，批量操作可能更久。

"创建完 issue 马上搜出来确认"的脚本会偶尔失败。已经知道 issue 的 key 时，直接 `GET /rest/api/2/issue/{key}` 更稳。一定要搜的话，新接口有 `reconcileIssues` 参数，最多传 50 个 issue id，要求结果对这些 issue 是最新的。

### 评论和 changelog 不全

搜索结果里每个 issue 最多带 20 条评论、40 条 changelog。要完整的，分别调 `GET /rest/api/2/issue/{key}/comment` 和 `GET /rest/api/2/issue/{key}/changelog`。

## Data Center 不用动

这次移除只发生在 Cloud。[Jira Data Center 11.0 的 REST 文档][dc-search]里，`GET` 和 `POST /rest/api/2/search` 都在，参数还是 `startAt` 和 `maxResults`，文档里也没有 `/search/jql`。

Data Center 上的脚本保持原样就行。照着上面改，请求的就是一个 Data Center 文档里没有的接口。

麻烦的是同一份脚本要同时对着 Data Center 和 Cloud 跑，迁移期间这很常见。这种情况我另写了一篇：[怎么写一份 Data Center 和 Cloud 都能跑的脚本][dc-cloud-post]。

## 用库的话

如果脚本本来就用了 Python 库，先看库里有没有新接口。下面的方法名以各库当前版本的源码为准，核对于 2026 年 11 月 15 日。

**[jira][pyjira]（pycontribs，3.10.5）**：`enhanced_search_issues()` 和 `approximate_issue_count()`。原来的 `search_issues()` 在 Cloud 上取第一页会转到新接口，`startAt` 不为 0 时抛 `JIRAError`。

**[atlassian-python-api][apa]（5.0.5）**：创建客户端时要传 `cloud=True`，然后用 `enhanced_jql()`、`enhanced_jql_get_list_of_tickets()` 和 `approximate_issue_count()`。原来的 `jql()` 在 `cloud=True` 时取第一页会转到新接口，`start` 不为 0 时抛 `ValueError`。

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

atlassian-python-api 的这三个新方法只能用在 Cloud 上，对着 Data Center 调会抛 `ValueError`。同一份脚本要兼顾两边，得自己判断该调哪个。

**[atlassian-api-py][aap]（2.0 及以上）**：这是我维护的，方法名在两边是同一套，库根据 URL 判断该走哪个接口。

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

URL 是 `*.atlassian.net` 时，这三个方法走 `/rest/api/2/search/jql` 和 `/rest/api/2/search/approximate-count`。把 URL 换成 Data Center 的地址，同样的三行走的是 `/rest/api/2/search`：

```python
jira = Jira(url="https://jira.company.com", token="your-personal-access-token")
```

不传 `fields` 时，它在 Cloud 上请求 `*navigable`，和 Data Center 的默认一致，免得同一段代码在两边拿到的字段不一样。

几点要交代清楚：

- 这个库很小。按 [pypistats][pypistats] 的数据，它上个月的下载量是 3,715 次，atlassian-python-api 是 800 多万次。它覆盖的接口也少得多。
- 2.0 把 import 的包名从 `atlassian` 改成了 `atlassian_api`，所以能和 atlassian-python-api 装在同一个环境里。从 1.x 升级要改 import。
- Cloud 这部分目前是对照 Atlassian 的 OpenAPI 规范、用 mock 服务器测的。针对真实 Cloud 站点的 nightly 测试还在搭。

本文里的 Python 代码都用 `responses` 模拟的 Jira 跑过，包括 410、翻页和最后一页没有 token 的情况。模拟的服务器是照 Atlassian 的文档写的，和真实站点可能有出入。如果它在你的站点上表现不一样，欢迎[提 issue][issues]。

[pyjira-issue]: https://github.com/pycontribs/jira/issues/2369
[change-2046]: https://developer.atlassian.com/changelog/#CHANGE-2046
[change-2598]: https://developer.atlassian.com/changelog/#CHANGE-2598
[search-docs]: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/
[search-docs-v2]: https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issue-search/
[v3-intro]: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#version
[api-token]: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
[pitfalls]: https://community.atlassian.com/forums/Jira-articles/Avoiding-Pitfalls-A-Guide-to-Smooth-Migration-to-Enhanced-JQL/ba-p/2985433
[dc-search]: https://developer.atlassian.com/server/jira/platform/rest/v11002/api-group-search/
[dc-cloud-post]: /zh-cn/posts/2026/atlassian-dc-cloud-scripts/
[pyjira]: https://github.com/pycontribs/jira
[apa]: https://github.com/atlassian-api/atlassian-python-api
[aap]: https://github.com/shenxianpeng/atlassian-api-py
[pypistats]: https://pypistats.org/packages/atlassian-api-py
[issues]: https://github.com/shenxianpeng/atlassian-api-py/issues
