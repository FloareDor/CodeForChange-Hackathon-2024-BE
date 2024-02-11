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
        projection = {"items": 0}
        for restaurant in self.restaurants_collection.find(projection=projection).sort("name"):
            restaurant["_id"] = str(restaurant["_id"])
            restaurants.append(restaurant)
        if restaurant:
            return JSONResponse(restaurants, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="No restaurants found")
        
    async def search_restaurants(self, request: Request, query: str):
        try:
            search_query = str(query).lower()
        except KeyError:
            raise HTTPException(status_code=400, detail="Missing or invalid 'query' parameter")

        filtered_restaurants = []
        projection = {"items": 0}
        # a regex pattern to match occurrences of the query anywhere within the name field
        regex_pattern = {"$regex": search_query, "$options": "i"}  # Case insensitive match
        query_filter = {"name": regex_pattern}
        
        for restaurant in self.restaurants_collection.find(query_filter, projection=projection).sort("name"):
            # print(restaurant)
            restaurant["_id"] = str(restaurant["_id"])
            filtered_restaurants.append(restaurant)

        if filtered_restaurants:
            return JSONResponse(filtered_restaurants, status_code=200)
        else:
            raise HTTPException(status_code=404, detail="No restaurants found")

        
    

