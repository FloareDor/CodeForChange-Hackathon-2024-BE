from fastapi import HTTPException, Header, Request
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
import json

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
        
    async def search_restaurants(self, request: Request):
        try:
            data_bytes = await request.body()
            data_str = data_bytes.decode('utf-8') 
            data = json.loads(data_str, strict=False)
            search_query = str(data["query"]).lower()
        except KeyError:
            raise HTTPException(status_code=400, detail="Missing or invalid 'query' parameter")

        filtered_restaurants = []
        for restaurant in self.restaurants_collection.find({"name": {"$regex": f"^{search_query}"}}).sort("name"):
            print(restaurant)
            restaurant["_id"] = str(restaurant["_id"])
            filtered_restaurants.append(restaurant)

        if filtered_restaurants:
            return JSONResponse(filtered_restaurants, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="No restaurants found")

