from fastapi import HTTPException, Header, Request
from fastapi.responses import JSONResponse
from bson import ObjectId
import re
import json
import httpx
import requests
from starlette.requests import Request

from utils.calscalculator import calculate_bmr, calculate_total_calories
from utils.authenticator import Authenticator
from utils.calscalculator import calculate_calories
from models.schemas import itemSchema, UserSchema, restaurantSchema

from utils.openAI import GPT

gpt = GPT()

class UserHandler:
	def __init__(self, db):
		self.db = db
		self.usersCollection = db["users"]
		self.restaurantsCollection = db["restaurants"]
		self.authenticator = Authenticator(db)

	def updateDailyGoals(self, user_data):
		print("user data: ", user_data )
		# Calculate daily goals based on user data
		userGoal = user_data["goal"]

		print("30")

		dailycalgoal = calculate_calories(user_data)
		dailyfatgoal = float(user_data["weight"])
		dailyproteingoal = float(user_data["weight"]) * 2
		dailycarbgoal = float(user_data["weight"]) * 5

		if userGoal == 0:
			dailycalgoal -= 500
		elif userGoal == 2:
			dailycalgoal += 500

		print("42222")

		user_data["dailycalgoal"] = dailycalgoal
		user_data["dailyfatgoal"] = dailyfatgoal
		user_data["dailyproteingoal"] = dailyproteingoal
		user_data["dailycarbgoal"] = dailycarbgoal
		

		return user_data

	async def putFitnessDetails(self, request: Request, authorization: str = Header(None)):
		print("req")
		print(request)
		print("autthth")
		print(authorization)
		print()
		if authorization is None:
			raise HTTPException(status_code=500, detail="No Authorization Token Received")
		try:
			# Authorize the request
			encodedUserData = await self.authenticator.Authorize(authorization=authorization)
			print(encodedUserData)
		except HTTPException as http_exception:
			# Handle authorization errors
			return JSONResponse({"detail": f"mock mee: {http_exception.detail}"}, status_code=http_exception.status_code)
		
		print("auth passed")
		try:
			data_bytes = await request.body()
			data_str = data_bytes.decode('utf-8') 
			data = json.loads(data_str, strict=False)

			# Parse user data and create UserSchema instance
			user_data = {
				"age": int(data["age"]),
				"gender": str(data["gender"]),
				"weight": float(data["weight"]),
				"height": float(data["height"]),
				"activeness": int(data["activeness"]),
				"goal": int(data["goal"])
			}

			user_schema = UserSchema(**user_data)

			# Update or insert user details into the database
			print(111111111111111111111111)
			
		  	# Assuming "sub" is the unique identifier
			# encodedUserData = await encodedUserData.json()  # Extract the JSON data from the JSONResponse object
			user_identifier = encodedUserData["sub"]
			print(111111111111111111111111)
			existingUser = False
			if user_identifier:
				# Update user details if user exists, otherwise insert new user
				existingUser = self.usersCollection.find_one({"sub": user_identifier})
					
				if existingUser is None:
					user_data["_id"] = ObjectId()
					user_data["sub"] = encodedUserData["sub"]
					user_data["name"] = encodedUserData["name"]
					user_data["email"] = encodedUserData["email"]
					user_data["picture"] = encodedUserData["picture"]
					result = self.usersCollection.insert_one(user_data)
					if result.acknowledged:
						print("Insertion successful.")
						# Additional handling if insertion was successful
					else:
						print("Insertion failed.")
					# if "sub" in userData:
					# 	userData.pop("sub")
					user_data["_id"] = str(user_data["_id"])
					print(2222222222)
					existingUser = self.usersCollection.find_one({"sub": user_identifier})
					print(2222222222)

				print(111111111111111111111111)
				print("existing user: ")
				print(existingUser)
				if existingUser is not None:
					user_data["sub"] = existingUser["sub"]
					user_data["_id"] = existingUser["_id"]
					user_data["name"] = encodedUserData["name"]
					user_data["email"] = encodedUserData["email"]
					user_data["picture"] = encodedUserData["picture"]
					print("333333")
					user_data = self.updateDailyGoals(user_data)
					print("333333")
					try:
						print(user_data)
						user_schema = UserSchema(**user_data)
					except:
						raise HTTPException(status_code=400, detail="invalid user data")

					self.usersCollection.update_one(
						{"sub": user_identifier},
						{"$set": user_schema.dict()}
					)
				else:
					raise HTTPException(status_code=400, detail="User account does not exist")

			else:
				raise HTTPException(status_code=400, detail="User identifier not found")

		except Exception as e:
			# Handle invalid user data or database errors
			raise HTTPException(status_code=400, detail=f"Invalid user data {e}", headers={"detail": str(e)})
		user_data["_id"] = str(user_data["_id"])
		return JSONResponse(user_data, status_code=200)
	
	async def healthifyMenu(self, request: Request, authorization: str = Header(None)):
		if authorization is None:
			raise HTTPException(status_code=500, detail="No Authorization Token Received")
		try:
			# Authorize the request
			encodedUserData = await self.authenticator.Authorize(authorization=authorization)
		except HTTPException as http_exception:
			# Handle authorization errors
			return JSONResponse({"detail": http_exception.detail}, status_code=http_exception.status_code)
		gptResult = ""
		print("passed auth")
		try:
			data_bytes = await request.body()
			data_str = data_bytes.decode('utf-8') 
			data = json.loads(data_str, strict=False)

			restaurantID = str(data["restaurant_id"])
			print(111111111111111111111111111)
			print(restaurantID)
			print(111111111111111111111111111)
			userPrompt = str(data["user_prompt"])
		except Exception as e:
			raise HTTPException(status_code=400, detail="invalid input data", headers={"detail": str(e)})
		print(restaurantID)
		try:
			user_identifier = encodedUserData["sub"]  # Assuming "sub" is the unique identifier
			print(user_identifier)
			print(user_identifier)
			print(user_identifier)
			existingUser = {}
			if user_identifier:
				# Update user details if user exists, otherwise insert new user
				existingUser = self.usersCollection.find_one({"sub": user_identifier})
				print(182)
				if existingUser is None:
					raise HTTPException(status_code=400, detail="User account does not exist")
			else:
				print(187)
				raise HTTPException(status_code=400, detail="User account identifier not found")
			print(185)
			# Update user details if user exists, otherwise insert new user
			existingRestaurant = self.restaurantsCollection.find_one({"_id": restaurantID})
			print("does restaurant exist?")
			if existingRestaurant is None:
				print("No")
			else:
				print("Yes")
			# print(existingRestaurant)
			if existingRestaurant is not None:
				gptResult = gpt.healthifyMenu(
					userPrompt, existingRestaurant["name"], existingRestaurant["items"], existingRestaurant["location"],existingUser["dailycalgoal"],existingUser["dailycarbgoal"], existingUser["dailyfatgoal"], existingUser["dailyproteingoal"]
				)
			else:
				raise HTTPException(status_code=400, detail="Restaurant not found")

		except Exception as e:
			print(e)
			# Handle invalid user data or database errors
			raise HTTPException(status_code=400, detail=f"error {e}", headers={"detail": str(e)})

		return JSONResponse({"result":gptResult}, status_code=200)
	

	

	

