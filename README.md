
- [Experimenting with kr8s](#experimenting-with-kr8s)
- [Lab environment](#lab-environment)
- [Collection of Observations](#collection-of-observations)
- [Overall Conclusion](#overall-conclusion)

# Experimenting with kr8s

I stumbled on the [kr8s project](https://github.com/kr8s-org/kr8s) recently and thought it might be a far easier way to integrate with Kubernetes than using the more traditional [Python Kubernetes Client](https://github.com/kubernetes-client/python).

In this repository I host a simple Project to deploy as a Pod (or perhaps even several deployments of different pods) to take kr8s for a test drive.

# Lab environment

The experimental code was tested on Ubuntu Server version 22.04 running [microk8s](https://microk8s.io/) with Kubernetes version 1.27

The version of `kr8s` I used at the time was v0.8.20

This repository depended on a Python virtual environment I created using the following commands in the repository root directory:

```shell
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
. venv/bin/activate
```

The required libraries for local testing can now be easily installed using the following command:

```shell
pip3 install -r requirements.txt
```

When installing the `kr8s` library, the following were installed as well (links are to project code repository as far as possible):

* [aiohttp](https://github.com/aio-libs/aiohttp) version 3.8.6
* [aiosignal](https://github.com/aio-libs/aiosignal) version 1.3.1
* [anyio](https://github.com/agronholm/anyio) version 4.0.0
* [async-timeout](https://github.com/aio-libs/async-timeout) version 4.0.3
* [attrs](https://github.com/python-attrs/attrs) version 23.1.0
* [certifi](https://github.com/certifi/python-certifi) version 2023.7.22
* [charset-normalizer](https://github.com/Ousret/charset_normalizer) version 3.3.0
* [exceptiongroup](https://github.com/agronholm/exceptiongroup) version 1.1.3
* [frozenlist](https://github.com/aio-libs/frozenlist) version 1.4.0
* [h11](https://github.com/python-hyper/h11) version 0.14.0
* [httpcore](https://github.com/encode/httpcore) version 0.18.0
* [httpx](https://github.com/encode/httpx) version 0.25.0
* [idna](https://github.com/kjd/idna) version 3.4
* [multidict](https://github.com/aio-libs/multidict) version 6.0.4
* [python-box](https://github.com/cdgriffith/Box) version 7.1.1
* [python-jsonpath](https://pypi.org/project/jsonpath/) version 0.10.1 (PyPi page)
* [pyyaml](https://github.com/yaml/pyyaml) version 6.0.1
* [sniffio](https://github.com/python-trio/sniffio) version 1.3.0
* [yarl](https://github.com/aio-libs/yarl) version 1.9.2

Some of these project probably deserves a deeper look as well... I need more time!

For making a practical example project, I also installed the [Python FastAPI library](https://fastapi.tiangolo.com/). The example project will basically expose a REST API that will return some information from the cluster.

The Python project was setup sing the _"[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)"_ guidelines.

The build process was automated in the `build.sh` file.

> **Warning**
> The current build script will attempt to push to my Docker Hub repo, Adjust to suite your needs !!!

Docker Hub repo for hosting the image: https://hub.docker.com/r/nicc777/kr8s_poc

The Kubernetes manifest in this repository will reference the image published on Docker Hub. For testing I used [Microk8s](https://microk8s.io/) running on a different machine. For this lab, any Kubernetes cluster should be fine as long as you have sufficient permissions to deploy resources as well as port forward to the Pod. Adding Ingress to the manifest is easy enough should it be required, since it is a very straight forward HTTP service.

The deployment will create a namespace called `kr8s-poc`.

To setup port forwarding, first get the pod name:

```shell
kubectl get pod -n kr8s-poc
```

An example may look like `kr8s-poc-deployment-76d5cf4995-clz8f`. You can now use this name to create a port forwarder:

```shell
kubectl port-forward kr8s-poc-deployment-76d5cf4995-clz8f -n kr8s-poc 9080:8080
```

To use the Swagger UI, open your web browser and point to http://localhost:9080/docs

You can also use curl: 

```shell
curl -s -X 'GET' -H 'accept: application/json' http://localhost:9080/namespaces
```

To get more information on pods running in a particular namespace try something like 

```shell
curl -s -X 'GET' -H 'accept: application/json' 'http://localhost:9080/namespace/kr8s-poc/pods'
```

To view the loge of the running pod, try:

```shell
kubectl logs kr8s-poc-deployment-76d5cf4995-clz8f -n kr8s-poc | grep -v "GET / HTTP/1.1"
```

# Collection of Observations

This is a list of observations I made as I went through the process of testing. 

| Observation Notes |
|-------------------|
| My first thought was about Kubernetes version compatibility, which can be tricky at times with API versions been promoted, deprecated or removed. Based on the note on the [installation page](https://docs.kr8s.org/en/latest/installation.html) of `kr8s`, they seem to try and hide the complexity by stating that the current version would be more or less supporting all the currently supported Kubernetes versions. It would therefore appear there are a number of clever tricks happening behind the scenes, but personally I would have likes some kind of a supported versions matrix. I also originally thought they created a wrapper for the Kubernetes Python CLient, but since his is not a dependency, it looks to me now that they integrate directly with the Kubernetes API. |
| I originally could not get logging to work properly, but it seems by supplying `uvicorn` with a YAML log configuration file works very well. |
| Since I use VSCode I kept my `.vscode` directory in the repo. This should be a good example of how to test Python application. For local testing I create a Python virtual environment in the project root directory using the command `python3 -m venv venv`. Once the virtual environment is activated, install dependencies with `pip3 install -r requirements.txt` |
| Authentication in cluster is picked up seamlessly by using a service account. From outside the cluster, by adding an environment variable `KUBECONFIG` pointing to the Kubernetes configuration file to use, credentials was also seamlessly picked up and used with no apparent issues. |
| I am not a big expert on asynchronous development, but the only issue I had was with variable scope. Originally I had the REST API return an error 500 even though the logs I had showed the result dictionary be created perfectly ok. It turns out that be creating a true copy (using the `copy` Python built-in library) to copy the initial result set from the `get()` call solved the problem. |

# Overall Conclusion

I found the [kr8s project](https://github.com/kr8s-org/kr8s) to be a lot quicker to develop in compared to the [Python Kubernetes Client](https://github.com/kubernetes-client/python). I think this may become may goto project for Kubernetes based development in the future.
