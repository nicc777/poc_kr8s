from fastapi import FastAPI
from kr8s.objects import Pod, Namespace
import kr8s
import logging
import sys
import json
import traceback


logger = logging.getLogger(__name__)
log_format = '%(asctime)s %(levelname)s - %(message)s'
log_level = logging.INFO
formatter = logging.Formatter(log_format)
h = logging.StreamHandler(sys.stdout)
h.setLevel(log_level)
h.setFormatter(formatter)
logger.addHandler(h)


app = FastAPI()


# This is also our liveness and readiness probe URI
@app.get("/")
async def root():
    return {"status": "ok"}


@app.get('/namespaces')
async def namespaces():
    namespaces = list()
    try:
        for namespace in await kr8s.asyncio.get('namespaces'):
            logger.info('namespace={}   type={}'.format(namespace, type(namespace)))
            namespace_d = namespace.__dict__
            logger.info('namespace_d={}   type={}'.format(json.dumps(namespace_d, default=str), type(namespace_d)))
            namespaces.append({"Name": namespace.metadata.name, "RawObject": namespace_d,})
    except:
        logger.error('EXCEPTION: {}'.format(traceback.format_exc()))
    return {"Namespaces": namespaces}


@app.get('/namespace/{namespace}/pods')
async def namespaced_pods(namespace):
    pods = list()
    try:
        for pod in await kr8s.asyncio.get("pods", namespace=namespace):
            logger.info('pod={}   type={}'.format(pod, type(pod)))
            pod_d = pod.__dict__
            logger.info('pod_d={}   type={}'.format(json.dumps(pod_d, default=str), type(pod_d)))
            pods.append({"Name": pod.metadata.name, "RawObject": pod_d,})
    except:
        logger.error('EXCEPTION: {}'.format(traceback.format_exc()))
    return {"Namespace": namespace,"Pods": pods,}

