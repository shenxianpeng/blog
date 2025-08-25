---
title: Praised by an Airflow Maintainer—The Rise of prek, a Rust Rewrite of pre-commit
summary: While browsing online yesterday, I stumbled upon a repository called `prek`, described as — ⚡ Better `pre-commit`, re-engineered in Rust. This piqued my interest, as `pre-commit`, being a widely used pre-commit tool, would undoubtedly benefit from improvements, especially in performance.
tags:
  - Python
  - pre-commit
date: 2025-08-13
author: shenxianpeng
---

While browsing online yesterday, I stumbled upon a repository called `prek`, described as — ⚡ Better `pre-commit`, re-engineered in Rust. This piqued my interest, as `pre-commit`, being a widely used pre-commit tool, would undoubtedly benefit from improvements, especially in performance.

Most interestingly, the author of `pre-commit` also posted on this project's Issue.  He initially expressed a desire for collaboration, then mentioned the project violated copyright (since fixed), and finally labeled it malicious, unethical, and plagiaristic.

Let's take a look at this post. I'll use Google Translate to help everyone understand.

![asottile](comment-1.png)

![j178](comment-2.png)

![asottile](comment-3.png)

![jbvsmo](comment-4.png)

![potiuk](comment-5.png)

Finally, after a comment from an Airflow Maintainer, the author added a ❤️ and locked the thread. (A perfect move!)

> Link here: https://github.com/j178/prek/issues/73

This situation is somewhat reminiscent of uv replacing pip, although I haven't seen such controversy before.  This might be because pip is maintained by numerous community volunteers, while `pre-commit` is more like Anthony Sottile's "personal" project. While open-source, the original author retains absolute control.

Furthermore, its derivative project pre-commit.ci is free for open-source projects but charges for private repositories ($10/month), startups ($20/month), and large organizations ($100/month).  A competitive alternative could impact its revenue.

Let me briefly introduce Anthony Sottile—he's the author of `pre-commit`, a core developer of `pytest-dev` and `tox-dev`, maintains `flake8`, is a PyCQA member, a GitHub star, etc. If you use Python, you've likely encountered projects he's involved in. He's also a YouTuber who streams programming. I initially learned about him through `pre-commit` and have watched his videos; his expertise is undeniable. However, as mentioned above, his interaction style within the `pre-commit` community has caused discomfort or displeasure for some.


## My Opinion

Unless `pre-commit`'s original author, Anthony Sottile, becomes more proactive and open, accelerating the development of `pre-commit-rs`, the threat from `prek` will continue to grow.  Current trends suggest `prek` is gaining significant momentum.

Based on the following points, I believe it has the potential to go far:

* **Author Influence:** The `prek` author is an active and influential open-source contributor, involved in and contributing to well-known projects like `encode/httpx`, `astral-sh/uv`, `astral-sh/rye`, possessing the capacity to gain long-term community trust and endorsement.
* **High-Profile Endorsement:** `prek` has received positive endorsement from prominent contributors such as Jarek Potiuk—a contributor and PMC member of Apache Airflow, which is actively preparing to switch to `prek`.
* **Community Image Difference:** Compared to the `pre-commit` author's "cold" style, which might limit the willingness of external contributors to participate; `prek`, on the other hand, heeded community suggestions and changed the project name from `prefligit` to `prek`, which I consider a better name—shorter and easier to remember and pronounce. This creates space for the rise of an alternative.
* **Community Need:** The community needs a project like `prek`, actively pushing for a Rust rewrite, to disrupt the status quo of `pre-commit`.

Unless Anthony Sottile makes a 180-degree turn, proactively inviting external contributors to accelerate the development of `pre-commit-rs`, and changing his existing community interaction style, this trend is unlikely to reverse in the short term. Overall, I am optimistic about `prek`'s future.


At the time of writing, I also saw the author posting the above conversation on V2EX and Twitter, attracting more attention.

![v2ex](v2ex.png)

![twitter](x.png)

I won't comment further on this—the open-source community is a stage for continuous exchange, discussion, and competition.

---

Please indicate the author and source when reprinting this article.  Do not use it for any commercial purposes.  Follow the WeChat official account "DevOps攻城狮".