import asyncio
from app.database.connection import connect_to_mongo, get_database, close_mongo_connection

async def main():
    await connect_to_mongo()
    db = get_database()
    student = await db.students.find_one({"rollNumber": "181"})
    print("Timeline:", student.get("timeline", [])[-1])
    print("Risk:", student.get("risk"))
    await close_mongo_connection()

asyncio.run(main())
