from json import load
from dotenv import load_dotenv
from os import getenv
import json
load_dotenv()
from motor import motor_asyncio

dbclient = motor_asyncio.AsyncIOMotorClient(getenv("MONGO_URI"))

Database = dbclient.RIDM

async def insert_one(collection, data):
    print(data)
    data = json.loads(json.dumps(data, default=str))
    return await Database.get_collection(collection).insert_one(data)

async def find_one(collection, key, value):
    query = {key: {"$eq": value}}
    document = await Database.get_collection(collection).find_one(query)
    document.pop("_id") if document else None
    return document