import logging
import sys
import os
import json
import traceback
import uvicorn
from fastapi import FastAPI
import kr8s


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
    result = dict()
    try:
        for namespace in await kr8s.asyncio.get('namespaces'):
            logger.info('namespace={}   type={}'.format(namespace, type(namespace)))
            namespace_d = namespace.__dict__
            logger.info('namespace_d={}   type={}'.format(json.dumps(namespace_d, default=str), type(namespace_d)))
            namespaces.append({"Name": namespace.metadata.name, "RawObject": namespace_d,})
        result = {"Namespaces": namespaces}
        logger.info('result={}'.format(result))
        logger.info('returning result: {}'.format(json.dumps(result, default=str)))
    except:
        logger.error('EXCEPTION: {}'.format(traceback.format_exc()))
    return result


@app.get('/namespace/{namespace}/pods')
async def namespaced_pods(namespace):
    pods = list()
    result = dict()
    try:
        for pod in await kr8s.asyncio.get("pods", namespace=namespace):
            logger.info('pod={}   type={}'.format(pod, type(pod)))
            pod_d = pod.__dict__
            logger.info('pod_d={}   type={}'.format(json.dumps(pod_d, default=str), type(pod_d)))
            pods.append({"Name": pod.metadata.name, "RawObject": pod_d,})
        result = {"Namespace": namespace,"Pods": pods,}
        logger.info('result={}'.format(result))
        logger.info('returning result: {}'.format(json.dumps(result, default=str)))
    except:
        logger.error('EXCEPTION: {}'.format(traceback.format_exc()))
    return result
    

if __name__ == '__main__':
    current_file_dir = os.path.dirname(os.path.realpath(__file__))   
    src_part = '{}src{}'.format(os.sep, os.sep)
    if src_part in current_file_dir:
        log_config = '{}'.format(os.sep).join(current_file_dir.split(os.sep)[0:-2])
        log_config = '{}{}logging_config.yaml'.format(log_config, os.sep)
        print('Using LOG config from {}'.format(log_config))
        uvicorn.run(app, host="0.0.0.0", port=9080, workers=1, log_config=log_config)
    else:
        print('Using DEFAULT LOG CONFIG')
        uvicorn.run(app, host="0.0.0.0", port=9080, workers=1)
    

