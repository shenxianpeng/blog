---
title: 2021—DevOps Engineer Learning Roadmap
summary: This article introduces the skills and tools required to become a DevOps engineer, covering knowledge in software development, operating systems, cybersecurity, containerization, continuous integration and deployment, and more.
tags:
  - DevOps
date: 2021-01-21
translate: fase
author: shenxianpeng
---

What does DevOps actually mean? 🤔

DevOps is a software development approach involving continuous development, continuous testing, continuous integration, deployment, and monitoring.  This series of processes spans the traditionally isolated development and operations teams, and DevOps seeks to eliminate the barriers between them.

Therefore, a DevOps engineer essentially works with both Development and Operations teams. It's the link between these two major parts.


## Concepts and Tools

DevOps encompasses concepts such as build automation, CI/CD, infrastructure as code, and many tools exist to implement these concepts.  The sheer number of these tools can lead to confusion and overwhelm.

The most important thing is to understand the concepts and find one specific tool to learn for each category. For example, once you know what CI/CD is and know how to use Jenkins, it will be easier to learn other similar alternative tools.

Let's take a look at the skills you need to master to learn DevOps.

### 1) Software Development Concepts

As a DevOps engineer, you won't be directly programming applications, but you'll need to understand the following concepts as you work closely with development teams to improve and automate their tasks:

* How developers work
* Which git workflow they are using
* How to configure applications
* Automated testing

### 2) Operating Systems

As a DevOps engineer, you are responsible for preparing the infrastructure environment required to deploy applications on the operating system. And since most servers are Linux servers, you need to understand the Linux operating system and be proficient in using the command line, so you need to know:

* Basic shell commands
* The Linux filesystem
* Server administration basics
* SSH key management
* Installing different tools on servers

### 3) Networking and Security

You also need to understand the basics of networking and security to configure infrastructure, such as:

* Configuring firewalls to protect applications
* Understanding how IP addresses, ports, and DNS work
* Load balancers
* Proxy servers
* HTTP/HTTPS

However, to draw a line between DevOps and IT Operations, you are not a system administrator.  Therefore, advanced knowledge isn't needed here; understanding and knowing the basics is sufficient. The IT aspects are the specialties of those SysAdmins, Networking, or Security Engineers.

### 4) Containerization

With containers becoming the new standard, you'll likely be running applications as containers, meaning you need a general understanding of:

* The concept of virtualization
* The concept of containers
* Which tool to learn? Docker—the most popular container technology today.

### 5) Continuous Integration and Deployment

In DevOps, all code changes (e.g., new features and bug fixes from developers) should be integrated into the existing application and continuously deployed to end-users in an automated manner. Therefore, establishing a complete CI/CD pipeline is a major task and responsibility of a DevOps engineer.

After completing a feature or bug fix, a pipeline running on a CI server (e.g., Jenkins) should be automatically triggered, which:

* Runs tests
* Packages the application
* Builds Docker images
* Pushes the Docker Image to an artifact repository, and finally
* Deploys the new version to the server (could be development, testing, or production servers)

Therefore, you need to learn skills here:

* Setting up CI/CD servers
* Build tools and package manager tools to run tests and package applications
* Configuring artifact repositories (e.g., Nexus, Artifactory)

Of course, more steps can be integrated, but this process represents the core of a CI/CD pipeline and is central to DevOps tasks and responsibilities.

Which tool to learn? Jenkins is one of the most popular. Others: Bamboo, Gitlab, TeamCity, CircleCI, TravisCI.

### 6) Cloud Providers

Today, many companies are using virtual infrastructure on the cloud instead of managing their own infrastructure. These are Infrastructure as a Service (IaaS) platforms that offer a range of services such as backup, security, load balancing, etc.

Therefore, you need to learn the services of cloud platforms. For example, for AWS, you should understand the basics of:

* IAM service—managing users and permissions
* VPC service—your private network
* EC2 service—virtual servers
* AWS offers many more services, but you only need to understand the services you actually need. For example, when a K8s cluster runs on AWS, you also need to learn the EKS service.

AWS is one of the most powerful and widely used, but also the most difficult.

Which tool to learn? AWS is the most popular. Other popular choices: Azure, Google Cloud, Alibaba Cloud, Tencent Cloud.

### 7) Container Orchestration

As mentioned earlier, containers are widely used, and in large companies, hundreds or thousands of containers are running on multiple servers, meaning these containers need to be managed in some way.

For this purpose, there are container orchestration tools, and the most popular is Kubernetes. Therefore, you need to learn:

* How Kubernetes works
* Managing and administering Kubernetes clusters
* And deploying applications within them

Which tool to learn? Kubernetes—the most popular, bar none.

### 8) Monitoring and Log Management

After the software is put into production, it's crucial to monitor it to track performance and detect problems in the infrastructure and application. Therefore, one of the responsibilities of a DevOps engineer is:

* Setting up software monitoring
* Setting up infrastructure monitoring, such as for your Kubernetes cluster and underlying servers.

Which tool to learn? Prometheus, Grafana...

### 9) Infrastructure as Code

Manually creating and maintaining infrastructure is time-consuming and error-prone, especially when you need to replicate infrastructure, such as for development, testing, and production environments.

In DevOps, the aim is to automate as much as possible, which is where "Infrastructure as Configuration" comes in. So, with IaC, we use code to create and configure infrastructure, and you need to understand two ways of IaC:

* Infrastructure provisioning
* Configuration management

Using these tools, infrastructure can be easily replicated and restored. Therefore, you should know one tool in each category to make your work more efficient and improve collaboration with colleagues.

Which tool to learn?

Infrastructure provisioning: Terraform is the most popular.
Configuration management: Ansible, Puppet, Chef.

### 10) Scripting Languages

A common task for a DevOps engineer is writing scripts and small applications to automate tasks. To be able to do this, you need to understand a scripting or programming language.

This could be an operating system-specific scripting language such as bash or Powershell.

It's also necessary to master an operating system-independent language such as Python or Go. These languages are more powerful and flexible.  Being proficient in one of these will make you more valuable in the job market.

Which tool to learn? Python: Currently the most in-demand, it's easy to learn, easy to read, and has many available libraries. Others: Go, NodeJS, Ruby.

### 11) Version Control

All of this automation logic is written as code, and version control tools (e.g., Git) are used to manage this code and configuration files.

Which tool to learn? Git—the most popular and widely used, bar none.

> [DevOps Roadmap [2021] - How to become a DevOps Engineer](https://dev.to/techworld_with_nana/devops-roadmap-2021-how-to-become-a-devops-engineer-1n9p)