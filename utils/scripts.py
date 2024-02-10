
from pymongo import MongoClient
import json
from bson import ObjectId

from os import environ as env

def initDB():
	ATLAS_URL = env.get("ATLAS_URL")
	LOCAL_DB = env.get("LOCAL_DB")
	client = MongoClient(ATLAS_URL)
	db = client["healthmymenu"]

	# restaurant collection
	professor_collection = db["restaurants"]
	professor_collection.delete_many({})

	# User collection
	user_collection = db["users"]
	user_collection.delete_many({})

	# items collection
	rating_collection = db["items"]
	rating_collection.delete_many({})

	return db

