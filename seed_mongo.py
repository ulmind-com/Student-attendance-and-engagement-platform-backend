import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def seed():
    uri = "mongodb+srv://officialactivity:admin1234@cluster0.cnpe2le.mongodb.net/kids_attendance"
    client = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=5000)
    db = client.get_database("kids_attendance")
    
    # Check if already seeded
    if await db.students.count_documents({}) > 0:
        print("Already seeded.")
        return

    students = [
        {"firstName": "Deepsundar", "lastInitial": "Das", "rollNumber": "181", "class_name": "Nursery-A", "section": "A", "parentStatus": "Pending"},
        {"firstName": "Aditya", "lastInitial": "Kumar", "rollNumber": "182", "class_name": "Nursery-A", "section": "A", "parentStatus": "Pending"},
        {"firstName": "Ratnadip", "lastInitial": "Shit", "rollNumber": "183", "class_name": "Nursery-A", "section": "A", "parentStatus": "Pending"},
        {"firstName": "Michael", "lastInitial": "Smith", "rollNumber": "A001", "class_name": "Grade-1", "section": "A", "parentStatus": "Pending"},
        {"firstName": "Emily", "lastInitial": "Johnson", "rollNumber": "A002", "class_name": "Grade-1", "section": "A", "parentStatus": "Pending"},
        {"firstName": "James", "lastInitial": "Williams", "rollNumber": "A003", "class_name": "Grade-1", "section": "A", "parentStatus": "Approved", "parentConsentUrl": "https://res.cloudinary.com/demo/image/upload/sample.jpg"},
        {"firstName": "Olivia", "lastInitial": "Brown", "rollNumber": "A004", "class_name": "Grade-1", "section": "A", "parentStatus": "Pending"},
        {"firstName": "William", "lastInitial": "Jones", "rollNumber": "A005", "class_name": "Grade-1", "section": "A", "parentStatus": "Approved", "parentConsentUrl": "https://res.cloudinary.com/demo/image/upload/sample.jpg"}
    ]
    
    for s in students:
        s.setdefault("timeline", [])
        s.setdefault("risk", "Stable")
        s.setdefault("attendance", 100)
        s.setdefault("status", "active")
        s.setdefault("parentsName", "Test Parent")
        s.setdefault("profilePhoto", "")
        await db.students.insert_one(s)
        
    print("Seeded successfully!")

asyncio.run(seed())
