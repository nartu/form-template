import pytest
import os, sys
import pymongo

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir)
# sys.path.insert(0,parent_dir)

# MongoDB health

# Params
mongo_server = None
# local
# mongo_server = "127.0.0.10:27017"

from db import Db

@pytest.fixture(scope="module")
def db():
    db = Db(mongo_server).get()
    print("Connect Mongo")
    yield db
    print("Disconnect Mongo")

def test_db_connection(db):
    assert db

def test_db_answer(db):
    assert Db(mongo_server).status()

def test_db_migration(db):
    count_documents = db.templates.count_documents({})
    assert count_documents > 0
