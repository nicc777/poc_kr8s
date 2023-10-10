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

# Collection of Observations

This is a list of observations I made as I went through the process of testing. 

| Observation Notes |
|-------------------|
| My first thought was about Kubernetes version compatibility, which can be tricky at times with API versions been promoted, deprecated or removed. Based on the note on the [installation page](https://docs.kr8s.org/en/latest/installation.html) of `kr8s`, they seem to try and hide the complexity by stating that the current version would be more or less supporting all the currently supported Kubernetes versions. It would therefore appear there are a number of clever tricks happening behind the scenes, but personally I would have likes some kind of a supported versions matrix. |
