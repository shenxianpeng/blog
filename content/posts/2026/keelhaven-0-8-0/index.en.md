---
title: Keelhaven Releases New Version—This Time, Updates Come from Real User Feedback
summary: |
  Most updates in Keelhaven 0.8.0 come from real user feedback: new backup destinations, customizable backup parameters, backup preview, and only keeping the latest N snapshots.
tags:
  - Keelhaven
  - Backup
  - macOS
authors:
  - shenxianpeng
date: 2026-09-09
series: ["My Open Source Projects"]
series_order: 5
---
On August 31st, I released Keelhaven; on September 3rd, I introduced it in the [previous post](../keelhaven/).

![Keelhaven](overview.png)

After that article was published, I started receiving feedback from real users: some sent emails, some opened GitHub Issue directly, some reposted on X, some gave a Star, and some even donated.

Thank you very much!!!

Some of these feedbacks were features I came up with myself while sitting at my computer, while others were usage scenarios I hadn't considered at all before. For example:

- One user provided feedback on five issues in a single Issue, including both bugs and features;
- Another user, who migrated from command-line `restic`, listed all the parameters they were using and asked if they could be used in Keelhaven.

In the newly released 0.8.0, many of these feedbacks have been implemented. I won't go into specific details here; if you're interested, you can directly install the latest version using the commands below.

```bash
brew install --cask shenxianpeng/tap/keelhaven
# or
curl -fsSL https://keelhaven.app/install.sh | bash
```

## Real User Feedback is the Most Valuable

When I first released it, I thought I had tested it thoroughly, and that the App was already quite easy to use. However, just a few days after its release, I started receiving user feedback.

Interestingly, most of the feedback wasn't about bugs, but rather feature requests, and many of these requests were things I hadn't thought of myself.

This made me realize even more: any tool, whether for developers or general users, only reveals its true usage scenarios once it actually starts being used. Many things are difficult to fully envision by simply thinking about them alone at a computer; only by putting the tool into users' hands and listening to their voices can one truly know what it still lacks.

So, I'd like to specially thank every user who took the time to write feedback.

I've seen all your feedback and am seriously considering it. Many have already been implemented, and the rest are still under consideration and design.

---

## If you use a Mac and are looking for a backup tool

Keelhaven is worth ten minutes of your time to try: select the folders you want to back up, the destination, and the backup frequency, then you can essentially forget about it.

It will back up on schedule in the background, periodically check the repository automatically, and only notify you when there's an issue.

Encryption is done locally, there's no account system; backups use the standard `restic` format, which can be restored at any time or migrated to other tools. It's open source, free, and available on macOS 14 or above. Its specific workings are described in more detail in the [previous post](../keelhaven/).

Official website: https://keelhaven.app
Source code: https://github.com/shenxianpeng/keelhaven

After trying it out, whether you find it useful or run into problems, you're welcome to let me know: you can send an email to `support@keelhaven.app`, or open a [GitHub Issue](https://github.com/shenxianpeng/keelhaven/issues); you can also leave a message on WeChat official account, Zhihu, or X. Especially if you post content related to Keelhaven on X, you can @ me, and I will also update relevant comments on its official website.

If you find it useful, please give it a Star and feel free to share it with friends who might need it.

Thank you to everyone who tried it, offered suggestions, or even donated.
