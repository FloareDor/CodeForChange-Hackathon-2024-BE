from fastapi import APIRouter, Request, Header
from typing import Dict, Any, List
from starlette.requests import Request
from fastapi.responses import JSONResponse
from utils.authenticator import Authenticator

from utils.scripts import initDB

db = initDB()
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

@router.get("/menu", response_model=List[Dict[str, Any]])
@limiter.limit("30/minute")
async def health(request: Request):
    return JSONResponse({"status": "ok"}, status_code=200)

@router.get("/restaurants", response_model=List[Dict[str, Any]])
@limiter.limit("30/minute")
async def health(request: Request):
    return JSONResponse({"status": "ok"}, status_code=200)

@router.get("/{restaurant}/items", response_model=List[Dict[str, Any]])
@limiter.limit("30/minute")
async def health(request: Request):
    return JSONResponse({"status": "ok"}, status_code=200)

# @router.get("/add-to-favourites", response_model=List[Dict[str, Any]])
# @limiter.limit("30/minute")
# async def health(request: Request):
#     return JSONResponse({"status": "ok"}, status_code=200)

# # Auth
# @router.post("/verify_user")
# @limiter.limit("12/minute")
# async def verifyUser(request: Request):
#     return await authenticator.Verify_user(request)




