# About

Serve to response any status of the http request and detailed request information.

# Requirement

- docker

# Deploy

Run up directly.

```shell
# Ensure that the container does not exist.
$ docker container rm -f httpstat;
$ docker container run -d --name httpstat -p 32767:32767 --restart=unless-stopped return1225/httpstat;

```

If you want to build by yourself, the `build.sh` is available.

```shell
$ sh build.sh build
```

If you need to debug and test locally, the `entrypoint.sh` is runnable.

```shell
$ sh entrypoint.sh dev
```
