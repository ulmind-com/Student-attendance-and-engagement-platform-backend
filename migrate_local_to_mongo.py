import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    mongo_uri = os.getenv("MONGODB_URI")
    if not mongo_uri:
        print("No MONGODB_URI found.")
        return
    
    print("Connecting to MongoDB Atlas...")
    client = AsyncIOMotorClient(mongo_uri)
    db = client["kids_attendance"]
    
    try:
        with open("data/database.json", "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Could not read local DB:", e)
        return

    print("Migrating Students...")
    students = data.get("students", [])
    if students:
        await db.students.delete_many({})
        for s in students:
            if "_id" in s:
                s["_id"] = str(s["_id"])
        await db.students.insert_many(students)
        print(f"Inserted {len(students)} students.")

    print("Migrating Emotional Questions...")
    questions = data.get("emotional_questions", [])
    if questions:
        await db.emotional_questions.delete_many({})
        await db.emotional_questions.insert_many(questions)
        print(f"Inserted {len(questions)} questions.")

    print("Migrating Attendance Logs...")
    attendance_log = data.get("attendance_log", [])
    if attendance_log:
        await db.attendance_log.delete_many({})
        for a in attendance_log:
            if "_id" in a:
                del a["_id"]
        if attendance_log:
            await db.attendance_log.insert_many(attendance_log)
        print(f"Inserted {len(attendance_log)} attendance records.")

    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
