from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import ArtifactEntity

import os
import sys
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd




from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e


    def export_collection_as_dataframe(self):

        '''
        read data from mongoDB collection and return as pandas dataframe

        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.client = pymongo.MongoClient(MONGO_URI)
            self.database = self.client[database_name]
            self.collection = self.database[collection_name]
            df = pd.DataFrame(list(self.collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            df = df.replace(to_replace="na", value=np.nan)
            logging.info(f"Dataframe shape: {df.shape}")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def export_dataframe_as_feature_store(self, df: pd.DataFrame) -> str:
        try:
            feature_store_dir = self.data_ingestion_config.feature_store_dir
            os.makedirs(feature_store_dir, exist_ok=True)
            feature_store_file_path = os.path.join(feature_store_dir, self.data_ingestion_config.file_name)
            df.to_csv(feature_store_file_path, index=False, header=True)
            return feature_store_file_path
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def split_data_as_train_test(self, df: pd.DataFrame) -> None:
        try:
            train_set, test_set = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio)
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            # create directories if not exist
            os.makedirs(os.path.dirname(train_file_path), exist_ok=True)
            os.makedirs(os.path.dirname(test_file_path), exist_ok=True)

            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
    
    
    def initiate_data_ingestion(self) -> ArtifactEntity:
        try:
            dataframe = self.export_collection_as_dataframe()
            self.export_dataframe_as_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact = ArtifactEntity(train_file_path=self.data_ingestion_config.training_file_path,
                                                    test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

        
    