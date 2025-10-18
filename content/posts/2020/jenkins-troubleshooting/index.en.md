---
title: Three Ways to Solve the Jenkins Declarative Pipeline "Method code too large" Exception
summary: This article introduces three methods to solve the "Method code too large" exception in Jenkins declarative pipelines, including moving steps outside the pipeline, migrating from declarative to scripted pipelines, and using Shared Libraries.
tags:
  - Pipeline
  - Troubleshooting
date: 2020-04-20
authors:
  - shenxianpeng
---

This is the second time I've encountered this problem while using Jenkins declarative pipelines. The first time I encountered this problem was in a Pipeline with about 600 lines of code, and I encountered the following error:

```java
org.codehaus.groovy.control.MultipleCompilationErrorsException: startup failed:
General error during class generation: Method code too large!

java.lang.RuntimeException: Method code too large!
	at groovyjarjarasm.asm.MethodWriter.a(Unknown Source)
	[...]
```

At that time, I also used Jenkins Shared Libraries, but the code organization was not very good, and many steps had not yet been separated as individual methods. To solve this problem, after a refactoring, I changed the original 600+ lines of Pipeline to the current 300+ lines. Unfortunately, as I continued to add features, I encountered this problem again recently.

The reason for this problem is that Jenkins puts the entire declarative pipeline into a single method, and at a certain size, the JVM fails due to `java.lang.RuntimeException: Method code too large!`. It seems that I have a method exceeding 64k.

There is already a ticket for this issue on Jenkins JIRA, but it has not been resolved yet. There are currently three solutions to this problem, but they each have their own advantages and disadvantages.

## Method 1: Move Steps into Methods Outside the Pipeline

Since mid-2017, you can declare a method at the end of the pipeline and then call it in the declarative pipeline.  This allows us to achieve the same effect as shared libraries, but avoids the maintenance overhead.

```pipeline
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                whateverFunction()
            }
        }
    }
}

void whateverFunction() {
    sh 'ls /'
}
```

| Advantages | Disadvantages |
|---|---|
| No extra maintenance cost | It's unknown if this solution will always be effective |
| All functionality is reflected in the Jenkinsfile | When a method is used in multiple Jenkinsfiles, this method will still write a lot of repetitive code |


## Method 2: Migrate from Declarative to Scripted Pipeline

Finally, we can migrate to a scripted pipeline. With it, we have complete freedom. But this will also lose the reason why we initially decided to use declarative pipelines. With a dedicated DSL, it's easy to understand how the pipeline works.

| Advantages | Disadvantages |
|---|---|
| No limitations | Requires significant refactoring |
|  | More prone to errors |
|  | May require more code to achieve the same functionality |


## Method 3: Use Shared Libraries

I currently use Jenkins Shared Libraries, with a shared library to execute some complex steps. Shared libraries seem to be widely used, especially in maintaining large and complex projects.

My final solution was to further reduce the code in the Pipeline. I also used the solution in Method 1, moving some steps outside the `Pipeline {}` block, especially those steps that are called repeatedly.

| Advantages | Disadvantages |
|---|---|
| Reduces a lot of duplicate code | Any modification will affect all references; it must be thoroughly tested before merging changes into referenced branches |
| Can be used in chunks | Difficult to understand what a step does if unfamiliar |
| The generated Jenkinsfile will be easier to read |  |


## Conclusion

Method 1: For single-repository integration, it can be implemented quickly, and most people can get started quickly.
Method 2: Scripted pipelines offer few limitations and are suitable for advanced users familiar with Java and Groovy, and those with more complex needs.
Method 3: For enterprise-level projects with many repositories that require extensive integration and a desire to learn about shared libraries, this method is recommended.