import requests

API_URL = "https://student-attendance-and-engagement.onrender.com/api/students"

students = [
    {"firstName": "Michael", "lastInitial": "Smith", "rollNumber": "A001", "class_name": "Grade-1", "section": "A", "parentsName": "John Smith", "parentStatus": "Pending"},
    {"firstName": "Emily", "lastInitial": "Johnson", "rollNumber": "A002", "class_name": "Grade-1", "section": "A", "parentsName": "Sarah Johnson", "parentStatus": "Pending"},
    {"firstName": "James", "lastInitial": "Williams", "rollNumber": "A003", "class_name": "Grade-1", "section": "A", "parentsName": "Robert Williams", "parentStatus": "Approved", "parentConsentUrl": "https://res.cloudinary.com/demo/image/upload/sample.jpg"},
    {"firstName": "Olivia", "lastInitial": "Brown", "rollNumber": "A004", "class_name": "Grade-1", "section": "A", "parentsName": "Michael Brown", "parentStatus": "Pending"},
    {"firstName": "William", "lastInitial": "Jones", "rollNumber": "A005", "class_name": "Grade-1", "section": "A", "parentsName": "David Jones", "parentStatus": "Approved", "parentConsentUrl": "https://res.cloudinary.com/demo/image/upload/sample.jpg"}
]

for s in students:
    res = requests.post(API_URL, json=s)
    print(f"Added {s['firstName']}: {res.status_code}")

