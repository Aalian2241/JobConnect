from dotenv import load_dotenv,find_dotenv
import os
from pymongo import MongoClient
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://AalPal:{password}@cluster0.hbcmcoq.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
project_database = client.test
_users = project_database.updateusers
# print(project_database.list_collection_names())

