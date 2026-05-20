import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test():
    uri = "mongodb+srv://officialactivity:admin1234@cluster0.cnpe2le.mongodb.net/kids_attendance"
    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    try:
        info = await client.server_info()
        print("SUCCESS! Connected to MongoDB.")
        db = client.get_database("kids_attendance")
        await db.test.insert_one({"test": "hello"})
        doc = await db.test.find_one({"test": "hello"})
        print("Read/Write test:", "SUCCESS" if doc else "FAILED")
    except Exception as e:
        print("FAILED to connect:", str(e))

asyncio.run(test())
