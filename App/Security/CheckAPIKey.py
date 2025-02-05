
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from DB.MongoDB import MongoDB
import json
import datetime
from bson.json_util import dumps
from decouple import config

# Initialize FastAPI API key header authentication
api_key_header = APIKeyHeader(name="access_token", auto_error=False)


# Initialize MongoDB
mongo = MongoDB(config("MONGO_USERNAME"), config("MONGO_PASSWORD"))


# FastAPI function to check API key validity
async def check_api_key(api_key: str = Depends(api_key_header)):
    """Check the validity of an API key. """
    if not api_key:
        raise HTTPException(status_code=400, detail="API Key is required")

    # Query MongoDB for API key details
    api_key_info = mongo.get_data("Users","Users-API-Keys", {"api_key": api_key},projection={"_id":0})

    if not api_key_info:
        raise HTTPException(status_code=400, detail="API Key Not Found")

    # Convert MongoDB document to dict
    api_key_info = json.loads(dumps(api_key_info))

    # Check if API key is expired
    expired_date = datetime.datetime.strptime(api_key_info["expired_date"], "%Y-%m-%d %H:%M:%S")
    if datetime.datetime.now() >= expired_date:
        raise HTTPException(status_code=400, detail="API Key Expired")

    # Check if API key usage limit is exceeded
    if api_key_info["usage"] <= 0:
        raise HTTPException(status_code=400, detail="API Key Limit Exceeded")


    return api_key_info
