###############################################################################
###                                                                         ###
###                           B A S E    I M A G E                          ###
###                                                                         ###
###############################################################################
FROM ubuntu:22.04 AS kr8s-poc-rest-base

LABEL Description="A container for the production hosting of the pykles REST API" Vendor="none" Version="0.1"

# Prep Python
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt-get upgrade -y
RUN apt install -y libterm-readline-gnu-perl apt-utils
RUN apt install -y python3 python3-pip python3-venv
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools 
RUN pip3 install --upgrade build

###############################################################################
###                                                                         ###
###                          B U I L D    I M A G E                         ###
###                                                                         ###
###############################################################################
FROM kr8s-poc-rest-base AS kr8s-poc-rest-build

LABEL Description="Intermediate image for building a Python App" Vendor="none" Version="1.0"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./ ./
RUN python3 -m build

# Install the app
RUN pip3 install dist/kr8s_poc-0.0.8.tar.gz

# Cleanup
RUN pip3 uninstall -y build setuptools virtualenv
RUN apt remove -y python3-pip python3-venv
RUN apt autoremove -y

###############################################################################
###                                                                         ###
###                          F I N A L    I M A G E                         ###
###                                                                         ###
###############################################################################


FROM kr8s-poc-rest-build AS kr8s-poc-rest

LABEL Description="A REST API for Kubernetes Node Resource Queries" Vendor="none" Version="0.8"

# Environment
ENV DEBUG "0"
ENV PORT 8080
WORKDIR /usr/src/app
EXPOSE 8080-8090
CMD uvicorn --host 0.0.0.0 --port $PORT --workers 4 --no-access-log kr8s_poc.main_server:app


