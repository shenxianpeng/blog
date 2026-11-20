---
title: "Atlassian Data Center 2029 年停止支持：怎么写一份 Data Center 和 Cloud 都能跑的脚本"
summary: |
  Jira 和 Confluence Data Center 在 2029 年 3 月 28 日停止支持，迁移期间很多团队两边同时在用，原来的自动化脚本搬到 Cloud 上会报错。这篇列出真正会影响脚本的差异：认证、用户标识、Jira 搜索、项目列表、Confluence 的 v2 API 和分页，然后给出一份两边通用的写法，先用 requests 手写，再用我维护的 atlassian-api-py 2.0。
tags:
  - Jira
  - Python
  - DevOps
authors:
  - shenxianpeng
date: 2026-11-15
draft: true
---

2026 年 10 月，我给自己维护的 [atlassian-api-py][aap] 加了 Atlassian Cloud 支持。按现在的源码数，同一个方法在 Data Center 和 Cloud 上要分开处理的，Jira 客户端 40 个方法里有 8 个，Confluence 的 23 个里有 18 个。

数据迁到 Cloud 之后，原来对着 Data Center 写的脚本会开始报 401 和 410。

这篇把会影响脚本的差异列出来，再给一份两边都能跑的写法。前半部分只用 `requests`，不需要装我的库。

## 时间表

按 [Atlassian 的公告][eol]：

| 日期 | 发生什么 |
|---|---|
| 2026-03-30 | 新客户不能再购买 Data Center 订阅 |
| 2028-03-30 | 老客户不能再新购或扩容 |
| 2029-03-28 | Data Center 停止支持，订阅到期，产品变成只读 |

受影响的是 Jira Software、Jira Service Management、Confluence 和 Crowd。Bitbucket 和 Bamboo Data Center 不在其中，这一点我在[另一篇][prev-post]里写过。

离 2029 年还有两年多，这期间不少团队会是一部分项目已经在 Cloud、一部分还在 Data Center。脚本要么维护两份，要么一份兼容两边。

## 认证

| | Data Center | Cloud |
|---|---|---|
| 推荐方式 | Personal access token，`Authorization: Bearer <token>` | 账号邮箱加 API token，Basic 认证 |
| 用户名密码 | 可以用 Basic 认证 | 已弃用 |

Data Center 的 [personal access token][pat] 从 Jira 8.14、Confluence 7.9 开始支持，放在 Bearer 头里，不需要用户名。

Cloud 的 [API token][basic-auth] 要和账号邮箱一起按 Basic 认证发送，文档里没有 Bearer 这种用法。把 Cloud 的 API token 照 Data Center 的习惯放进 Bearer 头，认证通不过，返回 401。

## 用户：username 变成 accountId

Cloud 的 REST API 里没有 `username` 和 `userKey`，用户只用 `accountId` 标识，这是 [2019 年开始执行的改动][gdpr]。凡是传用户的地方都要改：

| 操作 | Data Center | Cloud |
|---|---|---|
| 指派 issue | `{"name": "jdoe"}` | `{"accountId": "5b10ac8d82e05b22cc7d4ef5"}` |
| 查用户 | `GET /user?username=jdoe` | `GET /user?accountId=...` |
| 搜用户 | `GET /user/search?username=jo` | `GET /user/search?query=jo` |
| 加 watcher | 请求体是用户名 | 请求体是 accountId |
| JQL | `assignee = jdoe` | `assignee = 5b10ac8d82e05b22cc7d4ef5` |

返回的用户对象也跟着变了，Cloud 上没有 `name` 和 `key`。

脚本里写死的用户名，配置文件里的"默认指派给谁"，都得换成 accountId。可以用 `/user/search?query=` 查，它匹配显示名和邮箱的前缀。返回的内容受个人隐私设置影响，对方隐藏了邮箱时，结果里就看不到邮箱。

JQL 里的 `currentUser()` 两边都能用，不必改。

## Jira 搜索

Cloud 上 `/rest/api/2/search` 已经返回 410，要改用 `/rest/api/2/search/jql`：翻页从 `startAt` 换成 `nextPageToken`，响应里没有 `total`，默认只返回 `id`，JQL 必须带限制条件。

细节和常见的坑我单独写了一篇：[Jira Cloud 的 /rest/api/2/search 返回 410 Gone，脚本该怎么改][search-post]。

## Jira 的其他几处

- **项目列表。** Data Center 的 `GET /rest/api/2/project` 一次返回全部项目。Cloud 上这个接口[标记为弃用][project-docs]，替代的 `/rest/api/2/project/search` 是分页的，每页最多 100 个，用 `startAt` 翻页，看 `isLast` 判断结束。
- **创建版本。** Data Center 传项目 key（`"project": "OPS"`），Cloud 上 `project` 已弃用，要传数字的 `projectId`。
- **changelog。** Cloud 上 `expand=changelog` 只返回最近的一部分，完整历史要翻 `GET /rest/api/2/issue/{key}/changelog`。
- **富文本字段。** Cloud 的 v3 接口里，`description` 和评论正文是 Atlassian Document Format。继续用 `/rest/api/2/`，两边拿到的都是字符串。

## Confluence：v1 的内容接口没了

Confluence 的差别最大。Cloud 上的地址多一层 `/wiki`，而且 v1 的内容接口已经在 2025 年 5 月 1 日[被移除][change-2520]，调用返回 410。移除名单包括：

- 内容的增删改查：`/rest/api/content`、`/rest/api/content/{id}`
- 页面历史、子页面、评论、标签、附件列表
- 空间：`/rest/api/space`、`/rest/api/space/{key}`

替代品是 [REST API v2][confluence-v2]，地址在 `/wiki/api/v2`。除了路径，下面这些也变了。

| | Data Center（v1） | Cloud（v2） |
|---|---|---|
| 页面和博客 | 同一个 `/content`，用 `type` 区分 | 分开的 `/pages` 和 `/blogposts` |
| 空间 | 用 key，比如 `DOCS` | 用数字 id，先 `GET /spaces?keys=DOCS` 换出来 |
| 页面所属空间 | `space.key` | `spaceId` |
| 父页面 | `ancestors: [{"id": ...}]` | `parentId` |
| 正文 | `expand=body.storage` | `body-format=storage` |
| 翻页 | `start` 加 `limit` | `cursor`，`limit` 最大 250 |

还有两个默认行为不一样。v2 的页面列表默认包含已归档的页面，只要当前页面的话，得加 `status=current`。v2 创建页面时不给 `parentId`，要加 `root-level=true` 才会建在空间的根下。

CQL 搜索 `/rest/api/content/search` 不在移除名单里，Cloud 上还能用。

## 分页小结

| 接口 | Data Center | Cloud |
|---|---|---|
| Jira 搜索 | `startAt`，看 `total` | `nextPageToken`，没有就结束 |
| Jira 项目列表 | 不分页 | `startAt`，看 `isLast` |
| Confluence 列表 | `start`，看 `_links.next` | `cursor`，看 `_links.next` |

Confluence 两边有一个共同点，响应里有 `_links.next` 就说明还有下一页，没有就到头了。区别在这个链接里带的是 `start` 还是 `cursor`。

## 手写一个适配层

差异列出来不少，一个具体的脚本用到的往往只是其中几处。我的做法是把"现在连的是哪一种"收在一个地方，其他代码只看一个布尔值。

先是连接。Cloud 站点的域名是 `*.atlassian.net`，这里用它来判断。站点用了自定义域名的话，可以改成调 `GET /rest/api/2/serverInfo`，Cloud 返回的 `deploymentType` 固定是 `Cloud`。

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

然后每个有差异的操作写一个函数，分支留在函数里面：

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

业务代码就不用关心连的是哪边了：

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

这样写有两个好处。分支集中在几个函数里，迁移结束后删掉 Data Center 那一半就行。测试也好写，同一个函数对着两套 mock 各跑一遍。

它抹不平的是数据本身。`assign()` 的第二个参数在一边是用户名，在另一边是 accountId；`pages_in_space()` 返回的页面，一边有 `space`，另一边是 `spaceId`。函数名统一了，传进去和拿出来的东西还是两种。

## 用 atlassian-api-py

上面这层适配，[atlassian-api-py][aap] 2.0 已经做在库里了。Jira 和 Confluence 客户端根据 URL 判断是不是 Cloud，方法名和参数保持一套。

```sh
pip install atlassian-api-py
```

下面的例子需要 2.0 或更高版本。

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

同一段代码，Cloud 和 Data Center 的区别只在环境变量里。Cloud 设 `ATLASSIAN_USER` 和 `ATLASSIAN_API_TOKEN`，Data Center 设 `ATLASSIAN_PAT`。Confluence Cloud 的 URL 不用自己加 `/wiki`。

库在背后做的就是前面几节的事：

- `iter_issues()` 和 `count_issues()` 在 Cloud 上走 `/search/jql` 和 `/search/approximate-count`。
- `assign_issue()` 在 Cloud 上发 `accountId`。要查 accountId，用 `jira.search_users("jane@example.com")`。
- 在 Cloud 上误用了 `token=`，401 的报错里会提示改用邮箱加 API token。
- `get_projects()` 在 Cloud 上把 `/project/search` 的各页收齐，返回的还是一个列表。
- Confluence 的页面、空间、子页面、评论、标签方法在 Cloud 上走 v2，space key 到 id 的转换在库里完成。列表方法的返回值保持 v1 的外壳，也就是 `results`、`start`、`limit`、`size`，`start` 和 `limit` 在 Cloud 上被换算成 cursor。和 Data Center 一样，一次调用最多返回 `limit` 条，页面多的空间要自己用 `start` 往后翻。

站点用了自定义域名，库从 URL 认不出来时，传 `cloud=True`。

## 它做不到的

这个库不大，下面这些要先讲清楚：

- **Bitbucket 客户端只支持 Server 和 Data Center。** 传 `bitbucket.org` 的地址会直接抛 `ValueError`。Bitbucket Data Center 本来也不在这次停止支持的名单里。
- **没有 Jira Software 的看板和 sprint，也没有 Jira Service Management 的接口。** 需要这些的话，[atlassian-python-api][apa] 覆盖得全得多。
- **返回的对象在两边形状不同。** 库统一的是方法名、参数和列表的外壳，里面的对象是各自 API 的原样。Cloud 上的 Confluence 页面有 `spaceId`，没有 `space.key`；Cloud 上的 Jira 用户有 `accountId`，没有 `name`。读这些字段的代码还得自己分情况。
- **用户标识不会自动转换。** 给 `assign_issue()` 传用户名，在 Cloud 上会失败，库不会替你查 accountId。
- **`export_page_pdf()` 只支持 Data Center。** 在 Cloud 上调用会抛 `NotImplementedError`。
- **Cloud 这部分目前是对照 Atlassian 的 OpenAPI 规范、用 mock 服务器测的。** 针对真实 Cloud 站点的 nightly 测试还在搭。

本文的 Python 代码，手写的和用库的，都用 `responses` 模拟的 Data Center 和 Cloud 各跑过一遍。模拟的服务器是照 Atlassian 的文档写的，和真实站点可能有出入。

如果你的脚本里有这篇没提到、迁移时又确实坏了的地方，欢迎留言或者[提 issue][issues]，我想把它补进来。

[aap]: https://github.com/shenxianpeng/atlassian-api-py
[eol]: https://www.atlassian.com/licensing/data-center-end-of-life
[prev-post]: /zh-cn/posts/2026/jira-cloud-jenkins-bitbucket/
[pat]: https://confluence.atlassian.com/enterprise/using-personal-access-tokens-1026032365.html
[basic-auth]: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/
[gdpr]: https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-api-migration-guide/
[search-post]: /zh-cn/posts/2026/jira-cloud-search-410/
[project-docs]: https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-projects/#api-rest-api-2-project-get
[change-2520]: https://developer.atlassian.com/changelog/#CHANGE-2520
[confluence-v2]: https://developer.atlassian.com/cloud/confluence/rest/v2/intro/
[apa]: https://github.com/atlassian-api/atlassian-python-api
[issues]: https://github.com/shenxianpeng/atlassian-api-py/issues
