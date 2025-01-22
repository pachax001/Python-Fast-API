# db.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from config import MONGO_DB_NAME, MONGO_URI

class MongoConnection:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.client: AsyncIOMotorClient | None = None
        self.db = None

    async def connect(self):
        """Establish connection and test with 'ping'."""
        try:
            self.client = AsyncIOMotorClient(self.uri)
            await self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            print("Connected to MongoDB successfully.")
        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None

    async def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

mongo_conn = MongoConnection(MONGO_URI, MONGO_DB_NAME)
