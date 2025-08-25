---
title: Python Software Foundation (PSF) Infrastructure Overview
summary: This article introduces the infrastructure of the Python Software Foundation (PSF), including its services, providers, and team members, helping readers understand how the PSF supports the Python community.
tags:
  - Python
  - Infrastructure
author: shenxianpeng
date: 2024-05-28
---

The Python Software Foundation (PSF), perhaps familiar to many, is the organization behind the open-source Python programming language, dedicated to creating conditions for the growth and development of Python and the Python community.

Following our previous look at [Apache's infrastructure](2024/01/apache-services-and-tools/), this article explores the infrastructure of the Python Software Foundation (PSF) and what we can learn from it.


## PSF Infrastructure Overview

The PSF runs various infrastructure services to support its mission, ranging from the [PyCon website](https://us.pycon.org/) to the [CPython Mercurial](https://hg.python.org/) server. The goal of this page is to list all these services, where they run, and who the primary contacts are.

## Infrastructure Team

The Infrastructure Team is ultimately responsible for maintaining the PSF infrastructure. However, it does not need to be the infrastructure running the PSF services. In fact, most day-to-day operational services are handled by individuals not in the Infrastructure Team.  The Infrastructure Team assists in setting up new services and provides advice on individual services for maintainers. Its members also generally handle sensitive changes to global systems such as DNS. Current team members are:

* Alex Gaynor (has no responsibilities)
* Benjamin Peterson
* Benjamin W. Smith
* Donald Stufft
* Ee Durbin (PSF Director of Infrastructure)
* Noah Kantrowitz

The best way to contact the Infrastructure Team is by emailing infrastructure-staff@python.org.  They are also frequently contacted on the #python-infra channel on [Libera](https://libera.chat/).

## Infrastructure Providers

The PSF uses several different cloud providers and services for its infrastructure.

**Fastly**
Fastly generously donates its Content Delivery Network (CDN) to the PSF. Our highest-traffic services (namely PyPI, www.python.org, docs.python.org) use this CDN to improve end-user latency.

**DigitalOcean**
DigitalOcean is the current primary hosting provider for most of the infrastructure. Services deployed here are managed by Salt.

**Heroku**
Heroku hosts many CPython core workflow bots, short-lived or proof-of-concept applications, and other web applications suitable for deployment on Heroku.

**Gandi**
[Gandi](https://www.gandi.net/en-US) is our domain registrar.

**Amazon Route 53**
[Amazon Route 53](https://aws.amazon.com/route53/) hosts DNS for all domains, currently managed manually by infrastructure staff.

**DataDog**
[DataDog](https://www.datadoghq.com/) provides metrics, dashboards, and alerting.

**Pingdom**
[Pingdom](https://www.pingdom.com/) provides monitoring and alerts us when services are down.

**PagerDuty**
[PagerDuty](https://www.pagerduty.com/) is used for on-call rotation for PSF infrastructure staff on the front line, with volunteers as backup.

**OSUOSL**
The Oregon State University Open Source Lab hosts a hardware server for the PSF, speed.python.org, used for running benchmarks. This host is configured using [Chef](www.getchef.com) and their configuration management is located in the [PSF-Chef Git](https://github.com/python/psf-chef) repository.

### Data Centers

| PSF DC |    Provider   | Region |
|:------:|:-------------:|:------:|
| ams1   | Digital Ocean | AMS3   |
| nyc1   | Digital Ocean | NYC3   |
| sfo1   | Digital Ocean | SFO2   |

## Details of Various Services

This section lists PSF services, general information about their hosting, and contact information for their owners.

**Buildbot**
The [buildbot](https://www.python.org/dev/buildbot/) master is a service run by python-dev@python.org.  Specifically Antoine Pitrou and Zach Ware.

**bugs.python.org**
bugs.python.org is hosted by the PSF on DigitalOcean and powered by Roundup. It also deploys bugs.jython.org and issues.roundup-tracker.org.

**docs.python.org**
The Python documentation is hosted on DigitalOcean and served via Fastly. The maintainer is Julien Palard.

**hg.python.org**
The CPython Mercurial repositories are hosted on a Digital Ocean VM. The maintainers are Antoine Pitrou and Georg Brandl.

**mail.python.org**
The python.org Mailman instance is hosted at https://mail.python.org and SMTP (Postfix). All inquiries should be directed to postmaster@python.org.

**planetpython.org and planet.jython.org**
These are hosted on a DigitalOcean VM. The Planet code and configuration are hosted on GitHub and maintained by the team at planet@python.org.

**pythontest.net**
pythontest.net hosts the Python test suite. python-dev@python.org is ultimately responsible for its maintenance.

**speed.python.org**
speed.python.org is a [Codespeed instance](https://github.com/zware/codespeed) that tracks Python performance. The web interface is hosted on a DigitalOcean VM, benchmarks run on a strongfy machine at OSUOSL, and is scheduled by the Buildbot master. Maintained by speed@python.org and Zach Ware.

**wiki.python.org**
It's hosted on a DigitalOcean VM. The maintainer is Marc-André Lemburg.

**www.jython.org**
This is hosted from an Amazon S3 bucket. The setup is very simple and shouldn't require much tweaking, but infrastructure staff can adjust it if needed.

**www.python.org**
The main Python website is a Django application hosted on Heroku. Its source code can be found on [GitHub](https://github.com/python/pythondotorg) and issues with the website may be reported to the [GitHub issue tracker](https://github.com/python/pythondotorg/issues).  Python downloads (i.e., everything under https://www.python.org/ftp/) are hosted on a separate DigitalOcean VM. The entire website is behind Fastly. There is also https://staging.python.org for testing the site. http://legacy.python.org is a statically mirrored older website.

**PyCon**
The PyCon website is hosted on Heroku. The contact address is pycon-site@python.org.

**PyPI**
The Python Package Index carries the highest load of any PSF service. Its source code is available on [GitHub](https://github.com/pypa/warehouse).
All of its infrastructure is on AWS, configured by [pypi-infra](https://github.com/pypi/infra), fronted by Fastly. The infrastructure is maintained by Ee Durbin, Donald Stufft, and Dustin Ingram, and can be contacted at admin@pypi.org.

**PyPy properties**
The [PyPy website](pypy.org) is hosted on a DigitalOcean VM and maintained by pypy-dev@python.org.

> For the original article, please visit [this address](https://infra.psf.io/overview.html).

## Conclusion

From the PSF infrastructure, we see that they largely utilize cloud service providers and technologies to deploy their applications. Therefore, to participate in PSF infrastructure management, a deep understanding of technologies such as CDN, DigitalOcean, Heroku, Amazon Route 53, Amazon S3, DataDog, and Pingdom is required.

We envy those who can work full-time for open-source software, earning a salary doing what many programmers dream of.

But securing such a job requires matching skills and proactively seeking these opportunities to obtain a full-time open-source software engineer position.  Let's encourage each other!

---

Please indicate the author and source when reprinting this article. Please do not use it for any commercial purposes.  Welcome to follow the WeChat public account "DevOps攻城狮"