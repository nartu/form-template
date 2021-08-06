import sys
from typing import Optional, Dict, Tuple, Sequence
from fastapi import FastAPI, Body, Path, Form, Query, Request
from validation import fields_patterns
from get_from_db import FindTemplate
from migrate import Migrate
from db import Db

# fix ObjectId & FastApi conflict
import pydantic
from bson.objectid import ObjectId
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = FastAPI()


@app.get("/")
async def read_root():
    message = f"Test task! FastAPI running on Uvicorn with Gunicorn. Using Python {version}"
    return {"message": message}

@app.get("/db_status")
async def read_db():
    return Db().status()

# Clear db table
@app.delete("/clear_all")
async def delete_all_from_db():
    m = Migrate()
    r = m.clear_all()
    return r

# Add from file
@app.put("/migrate")
async def write_data_to_db():
    m = Migrate()
    r = m.from_file()
    return {'templates': r.get('count_all')}

# Add from file
@app.post("/save_to_file")
async def write_data_to_file():
    m = Migrate()
    r = m.to_file()
    return {r}

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
    return FindTemplate(fields_and_type).response_names()
