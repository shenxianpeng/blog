---
title: Why is my Jenkins Controller getting slower—Possible mistakes you might be making...
summary: This article introduces some best practices for Jenkins pipelines, aiming to help developers and operations personnel optimize Jenkins' performance and maintainability.
tags:
  - Jenkins
author: shenxianpeng
date: 2023-02-06
---

As the title says, the reason why your Jenkins Controller is getting slower might be due to not following some best practices in Jenkins pipeline writing.

Therefore, this article mainly introduces some best practices for Jenkins pipelines, aiming to show pipeline authors and maintainers some "anti-patterns" they might not have been aware of in the past.

I will try to list all possible Pipeline best practices and provide some concrete examples from practice.

## General Issues

### Ensure using Groovy code as glue in your pipeline

Use Groovy code to connect a set of actions rather than as the main functionality of the pipeline.

In other words, instead of relying on pipeline features (Groovy or pipeline steps) to drive the build process forward, use individual steps (e.g., `sh`) to accomplish multiple parts of the build.

Pipelines, as they increase in complexity (amount of Groovy code, number of steps used, etc.), require more resources (CPU, memory, storage) on the controller. Think of the Pipeline as a tool to accomplish the build, not the core of the build.

Example: Drive the build through its build/test/deploy process using a single Maven build step.

### Running shell scripts in Jenkins pipeline

Using shell scripts in Jenkins Pipeline can help simplify builds by merging multiple steps into a single stage. Shell scripts also allow users to add or update commands without having to modify each step or stage individually.

Using shell scripts in Jenkins Pipeline and its benefits:



### Avoid complex Groovy code in pipelines

For pipelines, Groovy code is always executed on the controller, meaning it consumes controller resources (memory and CPU).

Therefore, it is crucial to reduce the amount of Groovy code executed by the Pipeline (this includes any methods called on classes imported within the Pipeline).  Here are examples of the most common Groovy methods to avoid:

1. `JsonSlurper`: This function (and several other similar functions like `XmlSlurper` or `readFile`) can be used to read data from a file on disk, parse the data in that file into a `JSON` object, and then use `JsonSlurper().parseText(readFile("$LOCAL_FILE"))`. This command loads the local file into the controller's memory twice, which will require a lot of memory if the file is large or the command is executed frequently.

    Solution: Instead of using `JsonSlurper`, use a shell step and return standard output. This shell would look something like this: `def JsonReturn = sh label: '', returnStdout: true, script: 'echo "$LOCAL_FILE"| jq "$PARSING_QUERY"'`. This will use agent resources to read the file, and `$PARSING_QUERY` will help parse the file into a smaller size.

2. `HttpRequest`: This command is frequently used to fetch data from external sources and store it in variables. This is not ideal because not only is the request made directly from the controller (which might give erroneous results for things like HTTPS requests if the controller doesn't have certificates loaded), but the response to that request is stored twice.

    Solution: Use a shell step to perform the HTTP request from the agent, for example using tools like curl or wget, depending on the context. If the result must be in the Pipeline afterwards, try filtering the result on the agent side so that only the minimal necessary information has to be sent back to the Jenkins controller.

### Reduce repetition of similar pipeline steps

Combine pipeline steps into single steps as much as possible to reduce the overhead caused by the pipeline execution engine itself.

For example, if you run three shell steps consecutively, each step must start and stop, requiring the creation and cleanup of connections and resources on the agent and controller.

However, if you put all commands into a single shell step, only one step needs to be started and stopped.

Example: Instead of creating a series of `echo` or `sh` steps, combine them into one step or script.

### Avoid calling `Jenkins.getInstance`

Using `Jenkins.instance` or its accessor methods in a Pipeline or shared library is indicative of code abuse within that Pipeline/shared library.

Using the Jenkins API from a non-sandboxed shared library means the shared library is both a shared library and a kind of Jenkins plugin.

Great care must be taken when interacting with the Jenkins API from a pipeline to avoid serious security and performance issues. If you must use the Jenkins API in your build, the recommended approach is to create a minimal plugin in Java that implements a secure wrapper around the Jenkins API that you want to access using the Pipeline’s Step API.

Using the Jenkins API directly from a sandboxed Jenkinsfile means you might have to whitelist methods allowed by the sandbox protection, which can be bypassed by anyone who can modify the pipeline, which is a major security risk. Whitelisted methods run as the system user, with overall administrator permissions, which might give developers more permissions than expected.

Solution: The best solution is to address the calls being made, but if these calls must be done, then it’s best to implement a Jenkins plugin that can collect the data needed.


### Clean up old Jenkins builds

As a Jenkins administrator, deleting old or unnecessary builds can allow the Jenkins controller to run efficiently.

Resources for updates and related versions are reduced when you don't delete old builds.  `buildDiscarder` can be used in each pipeline job to keep a specific number of historical builds.

## Using Shared Libraries

### Don't override built-in pipeline steps

Stay away from custom/overridden pipeline steps as much as possible. Overriding built-in pipeline steps is the process of overriding standard pipeline APIs (like `sh` or `timeout`) using shared libraries. This practice is dangerous because pipeline APIs can change at any time, causing custom code to break or give different results than expected.

Troubleshooting is difficult when custom code breaks due to Pipeline API changes, because even if the custom code hasn't changed, it might not work after an API update.

Therefore, even if the custom code hasn’t changed, it doesn’t mean it will remain unchanged after an API update.

Finally, due to the widespread use of these steps throughout the pipeline, if something is coded incorrectly/inefficiently, the results can be catastrophic for Jenkins.

### Avoid large global variable declaration files

Having large variable declaration files can require significant memory with little to no benefit, since the file is loaded for every pipeline regardless of whether the variables are needed.

**It is recommended to create small variable files containing only the variables relevant to the current execution.**

### Avoid very large shared libraries

Using large shared libraries in Pipelines requires checking out a very large file before the Pipeline starts and loading the same shared library for every job currently executing, which leads to increased memory overhead and slower execution times.

## Answering Other Common Questions

### Handling concurrency in pipelines

Try to avoid sharing workspaces across multiple pipeline executions or multiple different pipelines. This practice might lead to unexpected file modifications or workspace renaming in each pipeline.

Ideally, the shared volume/disk is mounted in a separate location, files are copied from that location to the current workspace, and then, when the build completes, if any updates are done, files can be copied back.

Build different containers, creating the needed resources from scratch (cloud-type agents are very suitable for this). Building these containers will ensure the build process starts from scratch every time and is easily repeatable. If building containers doesn’t work, disable concurrency on the pipeline or use a lockable resources plugin to lock the workspace at runtime so that other builds can’t use it while it’s locked.

Warning: Disabling concurrency at runtime or locking the workspace might cause pipelines to be blocked while waiting for the resources if these resources are arbitrarily locked.

**Also, note that both these approaches take longer to get build results compared to using unique resources for each job.**

### Avoiding `NotSerializableException`

Pipeline code undergoes CPS transformation to allow pipelines to resume after a Jenkins restart. That is, you can shut down Jenkins or lose connection to the agent while the pipeline is running your script. When it comes back, Jenkins remembers what it was doing, and your pipeline script will resume execution as if it had never been interrupted. An execution technique called "Continuous Pipe Style (CPS)" plays a key role in resuming the pipeline. However, due to CPS transformation, some Groovy expressions will not work correctly.

Behind the scenes, CPS relies on being able to serialize the current state of the pipeline, as well as the remainder of the pipeline to be executed.
This means using unserializable objects in the pipeline will trigger a `NotSerializableException` being thrown when the pipeline tries to persist its state.

For more details and some examples that might be problematic, see [Pipeline CPS Method Mismatches](http://jenkins.io/redirect/pipeline-cps-method-mismatches).

Techniques to ensure pipelines run as expected will be described below.

### Ensuring persistent variables are serializable

During serialization, local variables are captured as part of the pipeline state. This means storing unserializable objects in variables during pipeline execution will result in a `NotSerializableException` being thrown.

### Don't assign unserializable objects to variables

One strategy is to leverage the fact that unserializable objects always infer their values “just in time” instead of computing their values and storing that value in a variable.

### Using `@NonCPS`

If necessary, you can use the `@NonCPS` annotation to disable CPS transformation for specific methods, whose body will not execute correctly if it is CPS transformed. Note that this also means the Groovy function will have to restart completely, since it is not transformed.

> Asynchronous pipeline steps (such as `sh` and `sleep`) are always CPS-transformed and cannot be used inside methods annotated with `@NonCPS`.  Generally, you should avoid using pipeline steps inside methods annotated with `@NonCPS`.

### Pipeline Durability

It is worth noting that changing the durability of the pipeline might result in `NotSerializableException` not being thrown where they would otherwise be thrown. This is because lowering the pipeline's durability via `PERFORMANCE_OPTIMIZED` means the pipeline's current state is persisted far less frequently. As a result, the pipeline never attempts to serialize unserializable values, and thus, no exception is thrown.

> The presence of this note is to inform the user of the root cause of this behavior. Setting the pipeline's durability to performance optimized is not recommended purely to avoid serialization problems.

* https://www.jenkins.io/doc/book/pipeline/pipeline-best-practices/
* https://www.cloudbees.com/blog/top-10-best-practices-jenkins-pipeline-plugin
* https://github.com/jenkinsci/pipeline-examples/blob/master/docs/BEST_PRACTICES.md
* https://devopscook.com/jenkinsfile-best-practices/

---

Please indicate the author and source when reprinting articles from this site, and do not use them for any commercial purposes.  Welcome to follow the WeChat public account "DevOps攻城狮"