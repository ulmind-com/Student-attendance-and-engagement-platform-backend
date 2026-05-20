import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = "mongodb+srv://ulmindsocialpvtltd_db_user:otAmPjxZYp75xH7E@cluster0.6h3vud7.mongodb.net/kids_attendance"

async def test():
    try:
        client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
        db = client["kids_attendance"]
        await db.command("ping")
        print("Connected to MongoDB!")
        count = await db.students.count_documents({})
        print(f"Students count: {count}")
    except Exception as e:
        print(f"Connection failed: {e}")

asyncio.run(test())
