from fastapi import HTTPException, Query


API_KEY = "qwerty"

async def verify_api_key(api_key: str = Query(..., description="Static API key")):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key