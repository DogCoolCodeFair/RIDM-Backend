from json import load
import motor.motor_asyncio
from dotenv import load_dotenv
from os import getenv
import json
load_dotenv()

dbclient = motor.motor_asyncio.AsyncIOMotorClient(getenv("MONGO_URI"))

Database = dbclient.RIDM

async def insert_one(collection, data):
    print(data)
    data = json.loads(json.dumps(data, default=str))
    return await Database.get_collection(collection).insert_one(data)