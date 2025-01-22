# app/routes/user_routes.py
from fastapi import APIRouter, Request, Depends, HTTPException
import bcrypt
from app.schemas import UserSchema, TokenSchema
from app.auth import create_access_token

router = APIRouter()

# Dependency to get the 'users' collection
def get_users_collection(request: Request):
    return request.app.state.users_collection

@router.post("/register")
async def register(user: UserSchema, users_collection=Depends(get_users_collection)):
    # Because this is Motor (async), use 'await' for DB operations
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode("utf-8")
    
    await users_collection.insert_one({"username": user.username, "password": hashed_password_str})

    return {"message": "User registered successfully"}

@router.post("/login", response_model=TokenSchema)
async def login(user: UserSchema, users_collection=Depends(get_users_collection)):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    stored_password = db_user["password"]
    if isinstance(stored_password, str):
        # Convert str -> bytes if necessary
        stored_password = stored_password.encode("utf-8")

    if not bcrypt.checkpw(user.password.encode("utf-8"), stored_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
