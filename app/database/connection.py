import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI", "")
DB_NAME = "kids_attendance"
USE_MONGO = bool(MONGO_URI)

# ── Persistent JSON Fallback Path ──
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "database.json"

# ──────────────────────────────────────────────
# JSON Persistence helpers (local fallback)
# ──────────────────────────────────────────────
def _load_db() -> dict:
    if DB_FILE.exists():
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return _default_db()

def _save_db(data: dict):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)

def _default_db() -> dict:
    return {
        "students": [
            {"_id": "1", "firstName": "Deepsundar", "lastInitial": "Das", "rollNumber": "181", "class": "Nursery-A", "class_name": "Nursery-A", "section": "A", "attendance": 100, "risk": "Stable", "parentStatus": "Pending", "timeline": [], "parentsName": "", "parentsPhone": "", "bloodGroup": ""},
            {"_id": "2", "firstName": "Aditya", "lastInitial": "Kumar", "rollNumber": "182", "class": "Nursery-A", "class_name": "Nursery-A", "section": "A", "attendance": 100, "risk": "Stable", "parentStatus": "Pending", "timeline": [], "parentsName": "", "parentsPhone": "", "bloodGroup": ""},
            {"_id": "3", "firstName": "Ratnadip", "lastInitial": "Shit", "rollNumber": "183", "class": "Nursery-A", "class_name": "Nursery-A", "section": "A", "attendance": 100, "risk": "Stable", "parentStatus": "Pending", "timeline": [], "parentsName": "", "parentsPhone": "", "bloodGroup": ""}
        ],
        "admin_users": [
            {"_id": "a1", "username": "admin", "password": "admin123", "role": "Super Admin", "created_at": "2026-05-15"}
        ],
        "attendance_log": [],
        "audit_log": [],
        "student_id_counter": 4,
        "admin_id_counter": 2
    }

# ──────────────────────────────────────────────
# MockCursor / MockResult (for JSON mode)
# ──────────────────────────────────────────────
class MockCursor:
    def __init__(self, data):
        self.data = data
    async def to_list(self, length=1000):
        return self.data[:length]

class MockResult:
    def __init__(self, inserted_id=None, matched_count=0, deleted_count=0):
        self.inserted_id = inserted_id
        self.matched_count = matched_count
        self.deleted_count = deleted_count

class PersistentCollection:
    def __init__(self, collection_name: str, id_counter_key: str):
        self.name = collection_name
        self.counter_key = id_counter_key

    def _docs(self):
        return _load_db().get(self.name, [])

    def _match(self, doc: dict, query: dict) -> bool:
        for k, v in query.items():
            if doc.get(k) != v:
                return False
        return True

    def find(self, query: dict = None):
        docs = self._docs()
        if not query:
            return MockCursor(list(docs))
        return MockCursor([d for d in docs if self._match(d, query)])

    async def find_one(self, query: dict):
        for doc in self._docs():
            if self._match(doc, query):
                return dict(doc)
        return None

    async def insert_one(self, document: dict):
        data = _load_db()
        docs = data.get(self.name, [])
        counter = data.get(self.counter_key, 1)
        doc = dict(document)
        doc["_id"] = str(counter)
        docs.append(doc)
        data[self.name] = docs
        data[self.counter_key] = counter + 1
        _save_db(data)
        return MockResult(inserted_id=doc["_id"])

    async def update_one(self, query: dict, update: dict, upsert: bool = False):
        data = _load_db()
        docs = data.get(self.name, [])
        for i, doc in enumerate(docs):
            if self._match(doc, query):
                if "$set" in update:
                    docs[i].update(update["$set"])
                if "$push" in update:
                    for k, v in update["$push"].items():
                        docs[i].setdefault(k, []).append(v)
                data[self.name] = docs
                _save_db(data)
                return MockResult(matched_count=1)
        if upsert:
            new_doc = dict(query)
            if "$set" in update:
                new_doc.update(update["$set"])
            return await self.insert_one(new_doc)
        return MockResult(matched_count=0)

    async def delete_one(self, query: dict):
        data = _load_db()
        docs = data.get(self.name, [])
        for i, doc in enumerate(docs):
            if self._match(doc, query):
                docs.pop(i)
                data[self.name] = docs
                _save_db(data)
                return MockResult(matched_count=1, deleted_count=1)
        return MockResult(matched_count=0, deleted_count=0)


# ──────────────────────────────────────────────
# MongoDB Motor Collection Wrapper
# ──────────────────────────────────────────────
class MongoCollectionWrapper:
    """Thin wrapper around Motor collection to normalize _id to str."""
    def __init__(self, collection):
        self.col = collection

    def find(self, query: dict = None):
        return self.col.find(query or {})

    async def find_one(self, query: dict):
        return await self.col.find_one(query)

    async def insert_one(self, document: dict):
        result = await self.col.insert_one(document)
        return MockResult(inserted_id=str(result.inserted_id))

    async def update_one(self, query: dict, update: dict, upsert: bool = False):
        result = await self.col.update_one(query, update, upsert=upsert)
        return MockResult(matched_count=result.matched_count)

    async def delete_one(self, query: dict):
        result = await self.col.delete_one(query)
        return MockResult(matched_count=result.deleted_count, deleted_count=result.deleted_count)


# ──────────────────────────────────────────────
# Database class
# ──────────────────────────────────────────────
class PersistentDatabase:
    def __init__(self, mongo_db=None):
        self._mongo_db = mongo_db
        self._using_mongo = mongo_db is not None

        if self._using_mongo:
            self.students = MongoCollectionWrapper(mongo_db["students"])
            self.admin_users = MongoCollectionWrapper(mongo_db["admin_users"])
            self.attendance_log = MongoCollectionWrapper(mongo_db["attendance_log"])
            self.classes = MongoCollectionWrapper(mongo_db["classes"])
            self.teachers = MongoCollectionWrapper(mongo_db["teachers"])
            self._audit_col = mongo_db["audit_log"]
            self._store_col = mongo_db["general_store"]
        else:
            self.students = PersistentCollection("students", "student_id_counter")
            self.admin_users = PersistentCollection("admin_users", "admin_id_counter")
            self.attendance_log = PersistentCollection("attendance_log", "att_id_counter")
            self.classes = PersistentCollection("classes", "classes_id_counter")
            self.teachers = PersistentCollection("teachers", "teachers_id_counter")

    # ── Helpers ──
    async def get_all_raw(self) -> dict:
        if self._using_mongo:
            doc = await self._store_col.find_one({"_id": "global_store"})
            return doc or {}
        return _load_db()

    async def save_raw(self, data: dict):
        if self._using_mongo:
            update_data = {k: v for k, v in data.items() if k not in ["_id"]}
            await self._store_col.update_one(
                {"_id": "global_store"}, {"$set": update_data}, upsert=True
            )
        else:
            _save_db(data)

    async def append_audit(self, action: str, entity: str, detail: str, performed_by: str = "admin"):
        entry = {
            "action": action,
            "entity": entity,
            "detail": detail,
            "performed_by": performed_by,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        }
        if self._using_mongo:
            await self._audit_col.insert_one(entry)
        else:
            data = _load_db()
            data.setdefault("audit_log", []).append(entry)
            _save_db(data)

    async def get_audit_log(self):
        if self._using_mongo:
            cursor = self._audit_col.find().sort("timestamp", -1)
            return await cursor.to_list(length=1000)
        return _load_db().get("audit_log", [])

    async def save_attendance_record(self, record: dict):
        if self._using_mongo:
            await self._mongo_db["attendance_log"].insert_one(record)
        else:
            data = _load_db()
            data.setdefault("attendance_log", []).append(record)
            _save_db(data)

    async def mark_absent_students(self, date_str: str):
        students_list = await self.students.find().to_list(length=1000)
        absent_count = 0
        for student in students_list:
            timeline = student.get("timeline", [])
            has_today = any(e.get("day") == "Today" or e.get("date") == date_str for e in timeline)
            if not has_today:
                timeline.append({"day": "Today", "emoji": "Absent", "score": 0, "alert": True, "status": "absent", "date": date_str})
                await self.students.update_one(
                    {"rollNumber": student["rollNumber"]},
                    {"$set": {"timeline": timeline, "risk": "Needs Attention"}}
                )
                absent_count += 1
                await self.save_attendance_record({
                    "roll_number": student.get("rollNumber"),
                    "name": f"{student.get('firstName')} {student.get('lastInitial')}",
                    "status": "absent",
                    "date": date_str
                })
        return absent_count


# ──────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────
_db_instance = None

def get_database() -> PersistentDatabase:
    global _db_instance
    if _db_instance is None:
        _db_instance = PersistentDatabase()
    return _db_instance

async def connect_to_mongo():
    global _db_instance

    if not MONGO_URI:
        print("[DB] No MONGODB_URI found — using local JSON database")
        _db_instance = PersistentDatabase()
        if not DB_FILE.exists():
            _save_db(_default_db())
        return

    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        print(f"[DB] Connecting to MongoDB Atlas...")
        client = AsyncIOMotorClient(
            MONGO_URI,
            serverSelectionTimeoutMS=10000,
            tlsAllowInvalidCertificates=False
        )
        db = client[DB_NAME]
        # Quick test
        await db.command("ping")
        _db_instance = PersistentDatabase(mongo_db=db)

        # Seed admin if not exists
        admin = await db.admin_users.find_one({"username": "admin"})
        if not admin:
            await db.admin_users.insert_one({
                "username": "admin", "password": "admin123",
                "role": "Super Admin", "created_at": datetime.utcnow().strftime("%Y-%m-%d")
            })
        print(f"[DB] ✅ Connected to MongoDB Atlas → {DB_NAME}")

    except Exception as e:
        print(f"[DB] ⚠️  MongoDB connection failed: {e}")
        print(f"[DB] 🔄 Falling back to local JSON database")
        _db_instance = PersistentDatabase()
        if not DB_FILE.exists():
            _save_db(_default_db())

async def close_mongo_connection():
    print("[DB] Database connection closed.")
