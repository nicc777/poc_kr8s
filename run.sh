#!/bin/sh

. venv/bin/activate

uvicorn --host 0.0.0.0 --port $PORT --workers 4 --no-access-log kr8s_poc.main_server:app