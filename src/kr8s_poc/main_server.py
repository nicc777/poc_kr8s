from fastapi import FastAPI

app = FastAPI()


# This is also our liveness and readiness probe URI
@app.get("/")
async def root():
    return {"status": "ok"}

