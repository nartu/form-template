import sys
from typing import Optional, Dict, Tuple, Sequence
from fastapi import FastAPI, Body, Path, Form, Query, Request
from validation import fields_patterns
from get_from_db import FindTemplate

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def read_root():
    message = f"Test task! FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

@app.get("/db_status")
async def read_db():
    return FindTemplate({}).db_status()

# На вход по урлу /get_form POST запросом передаются данные такого вида:
# f_name1=value1&f_name2=value2
# {
#     f_name1: FIELD_TYPE,
#     f_name2: FIELD_TYPE
# }
#
@app.post("/get_form")
async def data_in(request: Request):
    fields_and_data = request.query_params
    fields_and_type = fields_patterns(fields_and_data)
    return FindTemplate(fields_and_type).response()

# @app.post("/r/")
# def read_request(request: Request):
#     client_host = request.client.host
#     req = dict(request)
#     r = dir(request)
#     return {"client": request.client,
#      'path_params': request.path_params,
#      'query_params': request.query_params,
#      # 'r': r,
#      "r_type": request.method
#      }

@app.post("/items/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...)):
#     return {"username": username}
