from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional, List
from datetime import datetime

class itemSchema(BaseModel):
    _id: Optional[str] = None
    name: Optional[float] = None
    description: Optional[str] = None
    cals: Optional[float] = None
    carbs: Optional[float] = None
    fat: Optional[float] = None
    protein: Optional[float] = None
    # def __init__(self, **data):
    #     super().__init__(**data)
    #     # Additional validation logic can be placed here
    #     if self.courseQuality <= 0 or self.responsiveness <= 0 or self.teachingQuality <= 0 or self.helpfulness <= 0:
    #         raise ValueError('Rating values must be greater than 0')

class restaurantSchema(BaseModel):
    _id: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    logo: Optional[str] = None
    items: List[itemSchema] = []

class userSchema(BaseModel):
    _id: Optional[str] = None

    # google stuff
    sub: Optional[str]
    name: Optional[str]
    email: Optional[str]
    picture: Optional[str] = None

    # user data
    age: Optional[float] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    activity: Optional[str] = None
    
    # goals
    goal: Optional[int] = None
    dailycalgoal: Optional[float] = None
    dailycarbgoal: Optional[float] = None
    dailyfatgoal: Optional[float] = None
    dailyproteingoal: Optional[float] = None
    
	# tracking
    dailycals: Optional[float] = None
    dailycarbs: Optional[float] = None
    dailyfat: Optional[float] = None
    dailyprotein: Optional[float] = None
    

# class userSchema(BaseModel):
#     _id: Optional[str] = None
#     sub: Optional[str]
#     name: Optional[str]
#     email: Optional[str]
#     picture: Optional[str] = None
    