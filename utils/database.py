import json
from os import getenv
from typing import Union

from dotenv import load_dotenv
from fastapi import HTTPException

from models.user import Doctor, Patient

load_dotenv()
from motor import motor_asyncio

dbclient = motor_asyncio.AsyncIOMotorClient(getenv("MONGO_URI"))

Database = dbclient.RIDM


async def insert_one(collection, data):
    data = json.loads(json.dumps(data, default=str))
    return await Database.get_collection(collection).insert_one(data)


async def find_one(collection, key, value):
    query = {key: {"$eq": value}}
    document = await Database.get_collection(collection).find_one(query)
    document.pop("_id") if document else None
    return document

async def find_many(collection, key, value):
    query = {key: {"$eq": value}}
    documents = []
    async for document in Database.get_collection(collection).find(query):
        document.pop("_id")
        documents.append(document)
    return documents

async def update_one(collection, key, value, data):
    query = {key: {"$eq": value}}
    data = json.loads(json.dumps(data, default=str))
    await Database.get_collection(collection).replace_one(query, data)
    return await find_one(collection, key, value)


async def get_all_documents(collection):
    documents = []
    async for document in Database.get_collection(collection).find():
        document.pop("_id")
        documents.append(document)
    return documents


async def get_user(id) -> Union[Patient, Doctor]:
    data = await find_one("users", "id", id)
    if data:
        if data.get("isDoctor"):
            return Doctor(**data)
        else:
            return Patient(**data)
    else:
        raise HTTPException(status_code=404, detail="User not found")
