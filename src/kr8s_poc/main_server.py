import logging
import sys
import os
import json
import traceback
import uvicorn
from fastapi import FastAPI
import kr8s
import copy


logger = logging.getLogger(__name__)
log_format = '%(asctime)s %(levelname)s - %(message)s'
log_level = logging.INFO
formatter = logging.Formatter(log_format)
h = logging.StreamHandler(sys.stdout)
h.setLevel(log_level)
h.setFormatter(formatter)
logger.addHandler(h)


class KubeApi:
    def __init__(self) -> None:
        self.api = None


kube_api = KubeApi()
app = FastAPI()


# This is also our liveness and readiness probe URI
@app.get("/")
async def root():
    return {"status": "ok"}


@app.get('/namespaces')
async def namespaces():
    namespaces = list()
    result = dict()
    logger.info('FUNCTION namespaces() CALLED')
    try:
        for namespace in await kr8s.asyncio.get('namespaces', api=kube_api.api):
            namespace_data = dict()
            logger.info('namespace={}   type={}'.format(namespace, type(namespace)))
            namespace_raw_data = copy.deepcopy(namespace.raw)
            logger.debug('raw_data={}   type={}'.format(json.dumps(namespace_raw_data, default=str), type(namespace_raw_data)))
            if 'metadata' in namespace_raw_data:
                if 'creationTimestamp' in namespace_raw_data['metadata']:
                    namespace_data['CreateTimestamp'] = namespace_raw_data['metadata']['creationTimestamp']
                if 'labels' in namespace_raw_data['metadata']:
                    namespace_data['Labels'] = namespace_raw_data['metadata']['labels']
            namespaces.append({"Name": namespace.metadata.name, "Metadata": namespace_data,})
        result = {"Namespaces": namespaces}
        logger.debug('returning result: {}'.format(json.dumps(result, default=str)))
    except:
        logger.error('EXCEPTION: {}'.format(traceback.format_exc()))
    return result


@app.get('/namespace/{namespace}/pods')
async def namespaced_pods(namespace):
    pods = list()
    result = dict()
    logger.info('FUNCTION namespaced_pods() CALLED')
    try:
        for pod in await kr8s.asyncio.get("pods", namespace=namespace):
            pod_meta_data = dict()
            pod_status_data = dict()
            logger.info('pod={}   type={}'.format(pod, type(pod)))
            pod_raw_data = copy.deepcopy(pod.raw)
            logger.debug('tmp_raw_data={}   type={}'.format(json.dumps(pod_raw_data, default=str), type(pod_raw_data)))
            if 'metadata' in pod_raw_data:
                if 'creationTimestamp' in pod_raw_data['metadata']:
                    pod_meta_data['CreateTimestamp'] = pod_raw_data['metadata']['creationTimestamp']
                if 'labels' in pod_raw_data['metadata']:
                    pod_meta_data['Labels'] = pod_raw_data['metadata']['labels']
            if 'status' in pod_raw_data:
                pod_status_data = pod_raw_data['status']
            pods.append({"Name": pod.metadata.name, "Metadata": pod_meta_data, "Status": pod_status_data,})
        result = {"Namespace": namespace,"Pods": pods,}
        logger.debug('returning result: {}'.format(json.dumps(result, default=str)))
    except:
        logger.error('EXCEPTION: {}'.format(traceback.format_exc()))
    return result
    

if __name__ == '__main__':
    kube_config_file = os.getenv('KUBECONFIG', None)
    if kube_config_file is not None:
        kube_api.api = kr8s.api(kubeconfig=kube_config_file)
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
    print('DONE')
    

