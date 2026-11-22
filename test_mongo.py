import os

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient

uri = os.getenv("MONGO_DB_URL")
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
