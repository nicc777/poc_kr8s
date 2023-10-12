from fastapi import FastAPI
from kr8s.objects import Pod
import kr8s
import logging
import sys


def get_logger():
    logger = logging.getLogger(__name__)
    log_format = '%(asctime)s %(levelname)s - %(message)s'
    log_level = logging.INFO
    formatter = logging.Formatter(log_format)
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(log_level)
    h.setFormatter(formatter)
    logger.addHandler(h)
    return logger


app = FastAPI()


# This is also our liveness and readiness probe URI
@app.get("/")
async def root():
    return {"status": "ok"}


@app.get('/namespaces')
async def namespaces():
    namespaces = list()
    logger = get_logger()
    for namespace in await kr8s.asyncio.get('namespaces'):
        logger.info('namespace={}'.format(namespace))
        namespaces.append({"Name": namespace.metadata.name,})
    return {"Namespaces": namespaces}


@app.get('/namespace/{namespace}/pods')
async def namespaced_pods(namespace):
    pods = list()
    logger = get_logger()
    for pod in await kr8s.asyncio.get("pods", namespace=namespace):
        logger.info('pod={}'.format(pod))
        pods.append(
            {
                "Name": pod.metadata.name,
            }
        )
    return {
        "Namespace": namespace,
        "Pods": pods,
    }

