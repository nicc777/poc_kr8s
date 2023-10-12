from fastapi import FastAPI
from kr8s.objects import Pod
import kr8s


app = FastAPI()


# This is also our liveness and readiness probe URI
@app.get("/")
async def root():
    return {"status": "ok"}


@app.get('/namespaces')
async def namespaces():
    namespaces = list()
    for namespace in await kr8s.asyncio.get('namespaces'):
        namespaces.append(namespace)
    return {"Namespaces": namespaces}


@app.get('/namespace/{namespace}/pods')
async def namespaced_pods(namespace):
    pods = list()
    for pod in await kr8s.asyncio.get("pods", namespace=namespace):
        pods.append(pod.metadata.name)
    return {
        "Namespace": namespace,
        "Pods": pods,
    }

