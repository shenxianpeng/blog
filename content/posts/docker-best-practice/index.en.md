---
title: You Must Know These 17 Docker Best Practices!
summary: This article shares some best practices to follow when writing Dockerfiles and using Docker, including suggestions on multi-stage builds, image optimization, and security.
tags:
  - Dokerfile
  - Docker
date: 2022-01-12
author: shenxianpeng
---

This article shares some best practices to follow when writing Dockerfiles and using Docker. It's a long read, so consider bookmarking it to read later—you're guaranteed to learn a lot!

## Table of Contents

Dockerfile Best Practices

1. Use Multi-Stage Builds
2. Adjust the Order of Dockerfile Commands
3. Use Small Base Docker Images
4. Minimize the Number of Layers
5. Use Unprivileged Containers
6. Prefer `COPY` over `ADD`
7. Cache Python Packages to the Docker Host
8. Run Only One Process per Container
9. Prefer Array over String Syntax
10. Understand the Difference Between `ENTRYPOINT` and `CMD`
11. Add Health Checks `HEALTHCHECK`

Docker Image Best Practices

1. Docker Image Versioning
2. Don't Store Secrets in Images
3. Use a `.dockerignore` File
4. Inspect and Scan Your Dockerfiles and Images
5. Sign and Verify Images
6. Set Memory and CPU Limits


## Dockerfile Best Practices

### 1. Use Multi-Stage Builds

Leverage the power of multi-stage builds to create leaner and more secure Docker images. Multi-stage Docker builds ([multi-stage builds](https://docs.docker.com/develop/develop-images/multistage-build/)) allow you to divide your Dockerfile into several stages.

For example, you can have one stage for compiling and building your application, which can then be copied to a subsequent stage.  Since only the last stage is used to create the image, dependencies and tools related to building the application are discarded, leaving a lean, modular, production-ready image.

Web development example:



```dockerfile
# Temporary stage
FROM python:3.9-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# Final stage
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*
```

In this example, the GCC compiler is required when installing certain Python packages, so we add a temporary, build-time stage to handle the build stage.

Since the final runtime image doesn't contain GCC, it's leaner and more secure. Image size comparison:

```bash
REPOSITORY                 TAG                    IMAGE ID       CREATED          SIZE
docker-single              latest                 8d6b6a4d7fb6   16 seconds ago   259MB
docker-multi               latest                 813c2fa9b114   3 minutes ago    156MB
```

Let's look at another example:

```dockerfile
# Temporary stage
FROM python:3.9 as builder

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels jupyter pandas


# Final stage
FROM python:3.9-slim

WORKDIR /notebooks

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*
```

Image size comparison:

```bash
REPOSITORY                  TAG                   IMAGE ID       CREATED         SIZE
ds-multi                    latest                b4195deac742   2 minutes ago   357MB
ds-single                   latest                7c23c43aeda6   6 minutes ago   969MB
```

In summary, multi-stage builds can reduce the size of your production images, helping you save time and money.  Additionally, this will simplify your production containers.  Being smaller and simpler, they will have a relatively smaller attack surface.

### 2. Adjust the Order of Dockerfile Commands

Pay close attention to the order of your Dockerfile commands to leverage layer caching.

Docker caches each step (or layer) in a given Dockerfile to speed up subsequent builds. When a step changes, not only that step but all subsequent steps' cache will be invalidated.

For example:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY sample.py .

COPY requirements.txt .

RUN pip install -r /requirements.txt
```

In this Dockerfile, we copy the application's code before installing the requirements. Now, every time we change `sample.py`, the build will reinstall the packages. This is highly inefficient, especially when using Docker containers as development environments.  Therefore, putting frequently changing files towards the end of the Dockerfile is key.

> You can also prevent unnecessary cache invalidation by using a `.dockerignore` file to exclude unnecessary files from being added to the Docker build context and the final image. More on this later.

Therefore, in the Dockerfile above, you should move the `COPY sample.py .` command to the bottom as follows:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r /requirements.txt

COPY sample.py .
```

Note:

1. Always put layers that are likely to change as low as possible in the Dockerfile.
2. Combine multiple `RUN apt-get update`, `RUN apt-get install`, etc. commands into one. (This also helps reduce the image size, which will be mentioned shortly).
3. If you want to disable the cache for a given Docker build, you can add the `--no-cache=True` flag.

### 3. Use Small Base Docker Images

Smaller Docker images are more modular and secure. Smaller base Docker images build, push, and pull faster. They also tend to be more secure because they only include the necessary libraries and system dependencies required to run your application.

Which base Docker image should you use?  There's no one-size-fits-all answer; it depends on what you are doing. Here's a comparison of the size of various Docker base images for Python.

```bash
REPOSITORY   TAG                 IMAGE ID       CREATED      SIZE
python       3.9.6-alpine3.14    f773016f760e   3 days ago   45.1MB
python       3.9.6-slim          907fc13ca8e7   3 days ago   115MB
python       3.9.6-slim-buster   907fc13ca8e7   3 days ago   115MB
python       3.9.6               cba42c28d9b8   3 days ago   886MB
python       3.9.6-buster        cba42c28d9b8   3 days ago   886MB
```

While the Alpine flavor, based on Alpine Linux, is the smallest, it often leads to increased build times if you can't find pre-compiled binaries that work with it.  Therefore, you may end up having to build binaries yourself, which might increase the image size (depending on required system-level dependencies) and build time (due to having to compile from source).

> Read [Best Docker Base Images for Python Applications](https://pythonspeed.com/articles/base-image-python-docker-images/) and [Using Alpine Can Make Python Docker Builds 50x Slower](https://pythonspeed.com/articles/alpine-docker-python/) to learn more about why you might best avoid Alpine-based base images.

Ultimately, it's all about balance. When in doubt, start with the `*-slim` flavor, especially during development mode as you are building your application.  You want to avoid having to constantly update your Dockerfile to install necessary system-level dependencies as you add new `Python` packages. As you harden your application and Dockerfile for production, you might want to explore using Alpine for the final image of a multi-stage build.

Also, don't forget to regularly update your base images to improve security and performance. When a new version of a base image is released, e.g., `3.9.6-slim` --> `3.9.7-slim`, you should pull the new image and update your running containers to get all the latest security patches.


### 4. Minimize the Number of Layers

Try to combine `RUN`, `COPY`, and `ADD` commands because they create layers. Each layer adds to the size of the image because they are cached. Therefore, as the number of layers increases, so does the image size.

You can test this using the `docker history` command.

```bash
docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
dockerfile   latest    180f98132d02   51 seconds ago   259MB

docker history 180f98132d02

IMAGE          CREATED              CREATED BY                                      SIZE      COMMENT
180f98132d02   58 seconds ago       COPY . . # buildkit                             6.71kB    buildkit.dockerfile.v0
<missing>      58 seconds ago       RUN /bin/sh -c pip install -r requirements.t…   35.5MB    buildkit.dockerfile.v0
<missing>      About a minute ago   COPY requirements.txt . # buildkit              58B       buildkit.dockerfile.v0
<missing>      About a minute ago   WORKDIR /app
...
```

Notice the size. Only `RUN`, `COPY`, and `ADD` commands increase the image size, and you can reduce the size of the final image by combining commands whenever possible. For example:

```dockerfile
RUN apt-get update
RUN apt-get install -y gcc
```

Can be combined into a single `RUN` command:

```dockerfile
RUN apt-get update && apt-get install -y gcc
```

Thus, creating a single layer instead of two, thereby reducing the size of the final image. While reducing the number of layers is a good idea, it's more important that it's not a goal in itself but rather a side effect of reducing image size and build time.  In other words, instead of trying to micro-optimize every command, you should focus on the first three practices!!!

1. Multi-stage builds
2. The order of Dockerfile commands
3. And using a small base image.


#### Note

1. `RUN`, `COPY`, and `ADD` all create layers
2. Each layer contains the difference from the previous layer
3. Layers add to the final image size

#### Tip

1. Combine related commands
2. Remove unnecessary files during the `RUN` step in the creation process
3. Minimize running `apt-get upgrade` as it upgrades all packages to the latest versions.
4. For multi-stage builds, don't worry too much about over-optimizing commands in temporary stages

Finally, for better readability, it is recommended to sort multi-line arguments alphanumerically.

```dockerfile
RUN apt-get update && apt-get install -y \
    gcc \
    git \
    matplotlib \
    pillow  \
    && rm -rf /var/lib/apt/lists/*
```

### 5. Use Unprivileged Containers

By default, Docker runs container processes as root inside the container.  However, this is bad practice because processes running as root inside the container also run as root on the Docker host.

Therefore, if an attacker gains access to the container, they gain all root privileges and can perform several attacks against the Docker host, such as:

1. Copying sensitive information from the host's filesystem to the container
2. Executing remote commands

To prevent this, ensure your container processes run as a non-root user.

```dockerfile
RUN addgroup --system app && adduser --system --group app

USER app
```

You can go a step further and remove shell privileges, ensuring there is no home directory.

```dockerfile
RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

USER app
```

Verification

```bash
docker run -i sample id

uid=1001(app) gid=1001(app) groups=1001(app)
```

Here, the application inside the container is running under a non-root user.  However, remember that the Docker daemon and the container itself are still running with root privileges.

Be sure to check out running the Docker daemon as a non-root user for help running both the daemon and containers as a non-root user.

### 6. Prefer `COPY` over `ADD`

Unless you are sure you need the extra functionality that `ADD` provides, use `COPY`.

So what's the difference between `COPY` and `ADD`?

First, both commands allow you to copy files into a Docker image from a specific location.

```dockerfile
ADD <src> <dest>
COPY <src> <dest>
```

While they seem to do the same thing, `ADD` has some extra capabilities.

* `COPY` is used to copy local files or directories from the Docker host to the image.
* `ADD` can be used for the same thing, but it can also be used to download external files.  Additionally, if you use a compressed file (tar, gzip, bzip2, etc.) as the `<src>` argument, `ADD` will automatically extract the contents to the specified location.

```dockerfile
# Copy local file on host to destination
COPY /source/path  /destination/path
ADD /source/path  /destination/path

# Download external file and copy to destination
ADD http://external.file/url  /destination/path

# Copy and extract local compressed file
ADD source.file.tar.gz /destination/path
```

Finally, `COPY` is semantically clearer and easier to understand than `ADD`.

### 7. Cache Python Packages to the Docker Host

When a requirements file is changed, the image needs to be rebuilt to install new packages. Previous steps will be cached, as mentioned in minimizing the number of layers. Downloading all packages on every image rebuild causes significant network activity and requires a considerable amount of time.  It takes the same amount of time on every rebuild to download common packages across different builds.

For Python, you can avoid this by mapping the pip cache directory to a directory on the host. So on every rebuild, the cached versions persist, improving build speed.

Add a volume in your Docker run as `-v $HOME/.cache/pip-docker/:/root/.cache/pip` or as a mapping in your Docker Compose file.

The directory mentioned above is for reference only; make sure you are mapping the cache directory, not the site-packages (where built-in packages live).

Moving the cache from the docker image to the host can save you space in your final image.

```dockerfile

# omit ...

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
        pip install -r requirements.txt

# omit ...

```

### 8. Run Only One Process per Container

Why is it recommended to run only one process per container?

Let's say your application stack consists of two web servers and a database. While you could easily run all three from one container, you should run each service in a separate container for easier reusability and scaling of each individual service.

* Scalability - Because each service is in a separate container, you can horizontally scale just one of your web servers to handle more traffic as needed.
* Reusability - Maybe you have another service that needs a containerized database; you can simply reuse the same database container without having two unnecessary services along for the ride.
* Logging - Coupled containers make logging much more complex. (We will discuss this in more detail later in this article)
* Portability and Predictability - When containers have fewer parts working, it is much easier to make security patches or debug issues.

### 9. Prefer Array over String Syntax

You can use `CMD` and `ENTRYPOINT` commands in your Dockerfiles in array (exec) or string (shell) format

In Dockerfiles, you can use the `CMD` and `ENTRYPOINT` commands in array (exec) or string (shell) format

```dockerfile
# Array (exec)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

# String (shell)
CMD "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
```

Both are correct and achieve almost the same thing; however, you should use the exec format whenever possible.

Quoting from the [official Docker documentation](https://docs.docker.com/compose/faq/#why-do-my-services-take-10-seconds-to-recreate-or-stop):

* Make sure you use the exec form of `CMD` and `ENTRYPOINT` in your Dockerfile.
* For example, use `["program", "arg1", "arg2"]` instead of `"program arg1 arg2"`. Using the string form causes Docker to run your process using `bash`, which doesn't handle signals correctly. Compose always uses the JSON form, so don't worry if you override the command or entrypoint in your Compose file.

Therefore, since most shells don't handle signals to child processes, if you use the shell format, CTRL-C (which generates `SIGTERM`) might not stop a child process.

Example:

```dockerfile
FROM ubuntu:18.04

# BAD: String (shell) format
ENTRYPOINT top -d

# GOOD: Array (exec) format
ENTRYPOINT ["top", "-d"]
```

Both do the same thing. But notice that in the string (shell) format case, `CTRL-C` won't kill the process.  Instead, you will see `^C^C^C^C^C^C^C^C^C^C`.

Another caveat is that the string (shell) format carries the shell's PID, not the process itself.

```dockerfile
# Array format
root@18d8fd3fd4d2:/app# ps ax
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     0:00 python manage.py runserver 0.0.0.0:8000
    7 ?        Sl     0:02 /usr/local/bin/python manage.py runserver 0.0.0.0:8000
   25 pts/0    Ss     0:00 bash
  356 pts/0    R+     0:00 ps ax


# String format
root@ede24a5ef536:/app# ps ax
  PID TTY      STAT   TIME COMMAND
    1 ?        Ss     0:00 /bin/sh -c python manage.py runserver 0.0.0.0:8000
    8 ?        S      0:00 python manage.py runserver 0.0.0.0:8000
    9 ?        Sl     0:01 /usr/local/bin/python manage.py runserver 0.0.0.0:8000
   13 pts/0    Ss     0:00 bash
  342 pts/0    R+     0:00 ps ax
```


#### 10. Understand the Difference Between `ENTRYPOINT` and `CMD`

Should I use `ENTRYPOINT` or `CMD` to run the container process? There are two ways to run commands inside a container.

```dockerfile
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]

# and

ENTRYPOINT ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
```

Both essentially do the same thing: start the application using the `Gunicorn` server on `config.wsgi`, binding it to `0.0.0.0:8000`.

`CMD` is easily overwritten. If you run `docker run <image_name> uvicorn config.asgi`, the above `CMD` will be replaced with the new arguments.

For example, `uvicorn config.asgi`. To override the `ENTRYPOINT` command, you must specify the `--entrypoint` option.

```bash
docker run --entrypoint uvicorn config.asgi <image_name>
```

Here, it's clear that we are overriding the entrypoint. So it's recommended to use `ENTRYPOINT` instead of `CMD` to prevent accidentally overriding commands.

They can also be used together.  For example:

```dockerfile
ENTRYPOINT ["gunicorn", "config.wsgi", "-w"]
CMD ["4"]
```

When used together like this, the command run for launching the container becomes:

```bash
gunicorn config.wsgi -w 4
```

As mentioned above, `CMD` is easily overwritten.  Therefore, `CMD` can be used to pass arguments to the `ENTRYPOINT` command.  For instance, it's easy to change the number of workers, like so:

```bash
docker run <image_name> 6
```

This will launch the container with 6 Gunicorn workers instead of the default 4.


### 11. Add Health Checks `HEALTHCHECK`

Use `HEALTHCHECK` to determine if the process running inside the container is not only up and running but also "healthy."

Docker exposes an API to check the status of the running processes within the container; it provides information beyond just whether a process is "running" because "running" encompasses "it's running," "still starting up," and even "stuck in some infinite loop error state." You interact with this API via the [`HEALTHCHECK`](https://docs.docker.com/engine/reference/builder/#healthcheck) instruction.

For example, if you are serving a web application, you can use the following to determine if the `/` endpoint is up and able to handle service requests:

```dockerfile
HEALTHCHECK CMD curl --fail http://localhost:8000 || exit 1
```

If you run `docker ps`, you can see the status of the `HEALTHCHECK`.

Healthy example

```bash
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS                            PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   10 seconds ago   Up 8 seconds (health: starting)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

Unhealthy example

```bash
CONTAINER ID   IMAGE         COMMAND                  CREATED              STATUS                          PORTS                                       NAMES
09c2eb4970d4   healthcheck   "python manage.py ru…"   About a minute ago   Up About a minute (unhealthy)   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   xenodochial_clarke
```

You can go a step further and set up a custom endpoint solely for health checks, then configure `HEALTHCHECK` to test against the returned data.

For instance, if the endpoint returns a JSON response of `{"ping": "pong"}`, you can instruct `HEALTHCHECK` to verify the response body.

Here's how to view the health check status using `docker inspect`:

>Some output omitted here.

```bash
❯ docker inspect --format "{{json .State.Health }}" ab94f2ac7889
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2021-09-28T15:22:57.5764644Z",
      "End": "2021-09-28T15:22:57.7825527Z",
      "ExitCode": 0,
      "Output": "..."
```

You can also add health checks to your Docker Compose file:

```yml
version: "3.8"

services:
  web:
    build: .
    ports:
      - '8000:8000'
    healthcheck:
      test: curl --fail http://localhost:8000 || exit 1
      interval: 10s
      timeout: 10s
      start_period: 10s
      retries: 3
```

Options:

* `test`: The command to test.
* `interval`: The interval to test—that is, test every x time unit.
* `timeout`: The maximum time to wait for a response.
* `start_period`: When to start the health check. It can be used when other tasks are performed before the container is ready, such as running migrations.
* `retries`: The maximum number of retries before declaring the test as failed.

If you're using an orchestration tool other than Docker Swarm (like Kubernetes or AWS ECS), they very likely have their own internal systems for handling health checks. Refer to your specific tool's documentation before adding the `HEALTHCHECK` instruction.


## Docker Image Best Practices

### 1. Docker Image Versioning

Avoid using the `latest` tag for your images whenever possible.

If you rely on the `latest` tag (which isn't a real "tag" as it is applied by default when an image doesn't have an explicit tag), you can't tell from the image tag which version of your code is running.

Rollbacks become difficult, and it's easy to be overwritten (accidentally or maliciously). Tags, like your infrastructure and deployments, should be immutable.

So regardless of how you treat your internal images, you shouldn't use `latest` for base images, as you might inadvertently deploy a new version with breaking changes to production.

For internal images, use descriptive tags to more easily tell which version of the code is running, handle rollbacks, and avoid naming conflicts. For instance, you can use the following descriptors to compose a tag.

1. Timestamp
2. Docker image ID
3. Git commit hash
4. Semantic version

See also this answer in a Stack Overflow [question](https://stackoverflow.com/a/56213290/1799408) "Properly Versioning Docker Images" for more options.

For example:

```bash
docker build -t web-prod-b25a262-1.0.0 .
```

Here, we compose the tag using:

1. Project name: web
2. Environment name: prod
3. Git commit short hash: b25a262 (obtained via the command `git rev-parse --short HEAD`)
4. Semantic version: 1.0.0

Choosing a tagging scheme and sticking to it is crucial.  Because commit hashes readily link image tags to code, it's recommended to include them in your tagging scheme.

### 2. Don't Store Secrets in Images

Secrets are sensitive information such as passwords, database credentials, SSH keys, tokens, and TLS certificates. This information should not be placed in your images unencrypted because unauthorized users who gain access to the image can simply inspect the layers to extract keys.

Therefore, don't add plain-text secrets to your Dockerfiles, especially when you're pushing images to a public repository like Docker Hub!!

```dockerfile
FROM python:3.9-slim

ENV DATABASE_PASSWORD "SuperSecretSauce"
```

Instead, they should be injected via:

1. Environment variables (at runtime)
2. Build-time arguments (at build time)
3. Orchestration tools such as Docker Swarm (via Docker secrets) or Kubernetes (via Kubernetes secrets).

Additionally, you can help prevent secrets from being leaked by adding common secret files and folders to your `.dockerignore` file.

```bash
**/.env
**/.aws
**/.ssh
```

Finally, be explicit about which files are copied into the image instead of recursively copying all files.

```dockerfile
# Bad practice
COPY . .

# Good practice
COPY ./app.py .
```

Being explicit also helps limit cache invalidation.

#### Environment Variables

You can pass secrets via environment variables, but they are visible in all subprocesses, linked containers, and logs and via `docker inspect`.  They are also difficult to update.

```bash
docker run --detach --env "DATABASE_PASSWORD=SuperSecretSauce" python：3.9-slim

b25a262f870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239

docker inspect --format='{{range .Config.Env}}{{println .}}{{end}}' b25a262f870eb0fdbf03c666e7fcf18f9664314b79ad58bc7618ea3445e39239

DATABASE_PASSWORD=SuperSecretSauce
PATH=/usr/local/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
LANG=C.UTF-8
GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
python_version=3.9.7
python_pip_version=21.2.4
python_setuptools_version=57.5.0
python_get_pip_url=https://github.com/pypa/get-pip/raw/c20b0cfd643cd4a19246ccf204e2997af70f6b21/public/get-pip.py
PYTHON_GET_PIP_SHA256=fa6f3fb93cce234cd4e8dd2beb54a51ab9c247653b52855a48dd44e6b21ff28b
```

This is the most straightforward secret management approach. While not the most secure, it keeps honest people honest, as it provides a thin layer of protection, helping to keep secrets out of the gaze of curious wandering eyes.

Using shared volumes to pass secrets is a better solution, but they should be encrypted, via Vault or AWS Key Management Service (KMS), because they are saved to disk.

#### Build-Time Arguments

You can use build-time arguments to pass secrets, but these secrets are visible to those who can access the image via docker history.

Example

```dockerfile
FROM python:3.9-slim


ARG DATABASE_PASSWORD
```

Build

```bash
docker build --build-arg "DATABASE_PASSWORD=SuperSecretSauce" .
```

If you only need to use a secret temporarily as part of the build. For example, an SSH key for cloning a private repo or downloading a private package. You should use multi-stage builds because the builder's history is discarded by the temporary stage.

```dockerfile
# Temporary stage
FROM python:3.9-slim as builder

# Secret argument
arg ssh_private_key

# Install git
RUN apt-get update && \
    apt-get install -y --no-install-recommends git

# Clone repo using ssh key
RUN mkdir -p /root/.ssh/ && \
    echo "${PRIVATE_SSH_KEY}" > /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts && \
    ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN git clone git@github.com:testdrivenio/not-real.git


# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy repo from temporary image
COPY --from=builder /your-repo /app/your-repo

```

Multi-stage builds only preserve the history of the final image. You can use this for persistent secrets your application needs, such as database credentials.

You can also use the new `--secret` option in docker build to pass secrets to your Docker image, which aren't stored in the image.

```dockerfile
# "docker_is_awesome" > secrets.txt

FROM alpine

# Display the secret from the default secret location.
RUN --mount=type=secret,id=mysecret cat /run/secrets/mysecret
```

This will mount the secret from the `secrets.txt` file.

Building the image

```bash
docker build --no-cache --progress=plain --secret id=mysecret,src=secrets.txt .

# Output
...
#4 [1/2] FROM docker.io/library/alpine
#4 sha256:665ba8b2cdc0cb0200e2a42a6b3c0f8f684089f4cd1b81494fbb9805879120f7
#4 cached

#5 [2/2] RUN --mount=type=secret,id=mysecret cat /run/secrets/myecret
#5 sha256:75601a522ebe80ada66dedd9dd86772ca932d30d7e1b11bba94c04aa55c237de
#5 0.635 docker_is_awesome#5 DONE 0.7s

#6 export to image
```

Finally, check the history to see if the secret is leaked.

```bash
❯ docker history 49574a19241c
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
49574a19241c   5 minutes ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      5 minutes ago   RUN /bin/sh -c cat /run/secrets/mysecret # b…   0B        buildkit.dockerfile.v0
<missing>      4 weeks ago     /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      4 weeks ago     /bin/sh -c #(nop) ADD file:aad4290d27580cc1a…   5.6MB
```

#### Docker Secrets

If you are using Docker Swarm, you can manage secrets using Docker secrets.

For example, initialize Docker Swarm mode.

```bash
docker swarm init
```

Create a docker secret.

```bash
echo "supersecretpassword" | docker secret create postgres_password -
qdqmbpizeef0lfhyttxqfbty0

docker secret ls
ID                          NAME                DRIVER    CREATED         UPDATED
qdqmbpizeef0lfhyttxqfbty0   postgres_password             4 seconds ago   4 seconds ago
```

When a container is given access to the secret above, it will be mounted at `/run/secrets/postgres_password`. This file will contain the actual value of the secret in plain text.

Using other orchestration tools?

* AWS Secrets Manager with Kubernetes Secrets: [https://docs.aws.amazon.com/eks/latest/userguide/manage-secrets.html](https://docs.aws.amazon.com/eks/latest/userguide/manage-secrets.html)
* DigitalOcean Kubernetes - [Recommended steps to secure a DigitalOcean Kubernetes cluster](https://www.digitalocean.com/community/tutorials/recommended-steps-to-secure-a-digitalocean-kubernetes-cluster)
* Google Kubernetes Engine - [Using Secret Manager with other products](https://cloud.google.com/secret-manager/docs/using-other-products#google-kubernetes-engine)
* Nomad - [Vault integration and retrieving dynamic secrets](https://learn.hashicorp.com/tutorials/nomad/vault-postgres?in=nomad/integrate-