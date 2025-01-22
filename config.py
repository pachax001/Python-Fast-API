import os
from dotenv import load_dotenv

# Load environment variables from config.env
load_dotenv("config.env")





# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

WORKER_URL = os.getenv("WORKER_URL")
JWT_SECRET_KEY= os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM= os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
# Validate if all required configurations are loaded
required_env_vars = [
    "MONGO_URI","MONGO_DB_NAME","WORKER_URL","JWT_SECRET_KEY","JWT_ALGORITHM","ACCESS_TOKEN_EXPIRE_MINUTES"
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)  # Convert to int