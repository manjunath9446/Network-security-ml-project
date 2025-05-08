import sys
import os
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(f"MONGO_DB_URL: {MONGO_DB_URL}") # Good to print and verify it's loaded

import certifi # Keep this at the top with other imports

import pandas as pd
# import numpy as np # Not used in this snippet
import pymongo # Just pymongo is fine
from networksecurity.exception.exception import NetworksecurityException
# from networksecurity.logger.logger import logger # Not used in this snippet

class NetworkDataextract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworksecurityException(e, sys)

    def csv_to_json(self, filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworksecurityException(e, sys)

    def insert_mongodb(self, records_to_insert, database_name_arg, collection_name_arg): # Renamed args
        try:
            # MONGO_DB_URL should be loaded globally or passed in, already done globally
            # ca_path should also be available or defined
            ca_path = certifi.where()

            mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca_path)
            
            database_instance = mongo_client[database_name_arg]
            collection_instance = database_instance[collection_name_arg]
            
            result = collection_instance.insert_many(records_to_insert)
            print(f"Inserted {len(result.inserted_ids)} records.")
            return len(result.inserted_ids)
        except pymongo.errors.ConnectionFailure as e:
            print(f"MongoDB ConnectionFailure: {e}")
            raise NetworksecurityException(e, sys)
        except pymongo.errors.ConfigurationError as e:
            print(f"MongoDB ConfigurationError (check connection string or auth): {e}")
            raise NetworksecurityException(e, sys)
        except Exception as e:
            
            print(f"Generic exception in insert_mongodb: {e}")
            raise NetworksecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = r"E:\ML projects\fastapi\Network_data\Phishing_Legitimate_full.csv"
    DATABASE_NAME = "Manju" 
    COLLECTION_NAME = "Network_data" 

    networkobj = NetworkDataextract()
    
    print(f"Attempting to convert CSV: {FILE_PATH}")
    records_from_csv = networkobj.csv_to_json(filepath=FILE_PATH)
    # print(records_from_csv) # This can be very long, comment out if not needed for debugging
    print(f"Successfully converted {len(records_from_csv)} records from CSV.")

    print(f"Attempting to insert records into MongoDB: {DATABASE_NAME}.{COLLECTION_NAME}")
    no_of_records_inserted = networkobj.insert_mongodb(records_from_csv, DATABASE_NAME, COLLECTION_NAME)
    print(f"Successfully inserted {no_of_records_inserted} records into MongoDB.")