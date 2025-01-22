from app.auth import oauth2_scheme, verify_token
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
router = APIRouter()

def get_links_collection(request: Request):
    return request.app.state.links_collection

@router.get("/channels")
async def get_channels(
    token: str = Depends(oauth2_scheme),
    links_collection=Depends(get_links_collection)
):
    # Validate the token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Fetch channels from the collection
    channels = await links_collection.find(
        {},  # No filter, get all records
        {"user_id": 0, "username": 0, "link": 0, "created_at": 0, "_id": 0}  # Exclude fields
    ).to_list(100)
    return jsonable_encoder({"channels": channels})
