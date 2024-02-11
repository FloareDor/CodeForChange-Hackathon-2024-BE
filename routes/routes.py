from fastapi import APIRouter, Request, Header
from typing import Dict, Any, List
from starlette.requests import Request
from fastapi.responses import JSONResponse
from utils.authenticator import Authenticator

from handlers.restaurants import RestaurantHandler
from handlers.userHandler import UserHandler

from utils.scripts import initDB, insertSampleData

from fastapi import Query

db = initDB()
insertSampleData("data/Final_data.csv", db)
restaurantHandler = RestaurantHandler(db)
userHandler = UserHandler(db)
authenticator = Authenticator(db)

# rate limit imports
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address, config_filename=".rate")
router = APIRouter()

# Health check
@router.get("/", response_model=List[Dict[str, Any]])
@limiter.limit("30/minute")
async def health(request: Request):
    return JSONResponse({"status": "ok"}, status_code=200)

# Auth
@router.post("/verify_user")
@limiter.limit("12/minute")
async def verifyUser(request: Request):
    return await authenticator.Verify_user(request)

@router.post("/onboarding")
@limiter.limit("30/minute")
async def onboard(request: Request, authorization: str = Header(None)):
    return await userHandler.putFitnessDetails(request, authorization=authorization)

@router.get("/restaurants", response_model=List[Dict[str, Any]])
@limiter.limit("30/minute")
async def getRestaurants(request: Request, query: str = Query(None)):
    if query:
        return await restaurantHandler.search_restaurants(request, query)
    else:
        return await restaurantHandler.get_all_restaurants(request)

@router.get("/{restaurant}/items", response_model=List[Dict[str, Any]])
@limiter.limit("30/minute")
async def health(request: Request):
    return JSONResponse({"status": "ok"}, status_code=200)

@router.post("/healthify-menu")
@limiter.limit("30/minute")
async def onboard(request: Request, authorization: str = Header(None)):
    return await userHandler.healthifyMenu(request, authorization=authorization)

# @router.get("/add-to-favourites", response_model=List[Dict[str, Any]])
# @limiter.limit("30/minute")
# async def health(request: Request):
#     return JSONResponse({"status": "ok"}, status_code=200)

# # Auth
# @router.post("/verify_user")
# @limiter.limit("12/minute")
# async def verifyUser(request: Request):
#     return await authenticator.Verify_user(request)




