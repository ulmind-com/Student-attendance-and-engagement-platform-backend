from app.database.connection import _load_db, _save_db
import random

db = _load_db()

classes = ["Nursery", "LKG", "UKG", "Class 1", "Class 2"]
sections = ["A", "B", "C"]

for s in db.get("students", []):
    if "class" not in s:
        s["class"] = random.choice(classes)
    if "section" not in s:
        s["section"] = random.choice(sections)
    if "otp" not in s:
        s["otp"] = {
            "code": str(random.randint(1000, 9999)),
            "used": False,
            "generated_at": None
        }

_save_db(db)
print("Updated students.")
