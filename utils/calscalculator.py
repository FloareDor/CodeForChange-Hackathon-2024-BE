from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    sex: str
    weight: float
    height: float
    age: int
    activity_level: str

def calculate_bmr(sex, weight, height, age):
    if sex.lower() in ["female", "f"]:
        bmr = (weight * 10) + (height * 6.25) - (age * 5) - 161
    else:
        bmr = (weight * 10) + (height * 6.25) - (age * 5) + 5
    return int(bmr)

def calculate_total_calories(bmr, activity_level):
    activity_multipliers = {
        "sedentary": 1.25,
        "light": 1.375,
        "moderate": 1.550,
        "active": 1.725
    }
    return bmr * activity_multipliers[activity_level]

@app.post("/calculate-calories/")
async def calculate_calories(user_input: UserInput):
    bmr = calculate_bmr(user_input.sex, user_input.weight, user_input.height, user_input.age)
    total_calories = calculate_total_calories(bmr, user_input.activity_level)
    return {"daily_calories_intake": total_calories}