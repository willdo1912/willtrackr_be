import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("MONGO_URL")
client = pymongo.MongoClient(url)

db = client["willtrackr"]
