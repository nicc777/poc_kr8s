#!/bin/sh

docker build --no-cache -t kr8s_poc .
export IMAGE_ID=`docker image ls | grep kr8 | awk '{print $3}' | head -1`
export KR8S_VERSION=`cat pyproject.toml | grep version | awk -F\" '{print $2}'`
docker tag $IMAGE_ID nicc777/kr8s_poc:v$KR8S_VERSION ; docker tag $IMAGE_ID nicc777/kr8s_poc:latest
docker push nicc777/kr8s_poc:v$KR8S_VERSION ; docker push nicc777/kr8s_poc:latest

