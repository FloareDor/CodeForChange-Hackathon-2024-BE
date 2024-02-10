from fastapi import HTTPException, Header, Request
from fastapi.responses import JSONResponse
from bson import ObjectId
import re

from utils.authenticator import Authenticator

class RestaurantHandler:
	def __init__(self, db):
		self.db = db
		self.restaurants_collection = db["restaurants"]
		self.authenticator = Authenticator(db)

	async def get_all_restaurants(self, request: Request):
		restaurants = []
		for restaurant in self.restaurants_collection.find().sort("name"):
			restaurant["_id"] = str(restaurant["_id"])
			restaurants.append(restaurant)
		if restaurant:
			return JSONResponse(restaurants, status_code=200)
		else:
			raise HTTPException(status_code=404, detail="No professors found")
