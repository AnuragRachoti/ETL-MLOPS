import os
import sys

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_DB_URL")

import certifi
#ca - certificate authoroties
ca = certifi.where()

import numpy as np
import pandas as pd
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def csv_to_json(self, csv_file_path, json_file_path):
        try:
            data = pd.read_csv(csv_file_path)
            data.reset_index(drop=True, inplace=True)
            records = data.to_dict(orient="records")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def insert_records_to_mongo(self, records, db_name, collection_name):
        try:
            self.db_name = db_name
            self.collection_name = collection_name
            self.records = records

            self.client = MongoClient(MONGO_URI, tlsCAFile=ca)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            self.collection.delete_many({})
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = 'ANURAG-DB'
    COLLECTION = 'NETWORK-DATA'
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json(FILE_PATH, "Network_Data/phisingData.json")
    no_of_records = networkobj.insert_records_to_mongo(records, DATABASE, COLLECTION)
    print(f"Inserted {no_of_records} records into MongoDB collection '{COLLECTION}' in database '{DATABASE}'.") 







print("Attempting to connect to MongoDB...", MONGO_URI)
if __name__ == "__main__":
    client = MongoClient(MONGO_URI)
    try:
        client.admin.command("ping")
        print("Connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
    finally:
        client.close()