import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

# ── Persistent Storage Path ──
DATA_DIR = Path(__file__).parent.parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "database.json"
AUDIT_FILE = DATA_DIR / "audit_log.json"

# ──────────────────────────────────────────────
# JSON Persistence helpers
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
        "attendance_log": [],   # daily attendance records
        "audit_log": [],        # admin actions (add/delete/update)
        "student_id_counter": 4,
        "admin_id_counter": 2
    }

def _append_audit(action: str, entity: str, detail: str, performed_by: str = "admin"):
    data = _load_db()
    data.setdefault("audit_log", []).append({
        "action": action,
        "entity": entity,
        "detail": detail,
        "performed_by": performed_by,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })
    _save_db(data)


# ──────────────────────────────────────────────
# MockCursor / MockResult
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


# ──────────────────────────────────────────────
# Persistent Collection
# ──────────────────────────────────────────────
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
# Database class
# ──────────────────────────────────────────────
class PersistentDatabase:
    def __init__(self):
        # Seed default data if DB file doesn't exist
        if not DB_FILE.exists():
            _save_db(_default_db())
            print(f"[DB] Fresh database created at {DB_FILE}")
        else:
            print(f"[DB] Loaded existing database from {DB_FILE}")

        self.students     = PersistentCollection("students",     "student_id_counter")
        self.admin_users  = PersistentCollection("admin_users",  "admin_id_counter")
        self.attendance_log = PersistentCollection("attendance_log", "att_id_counter")

    # ── Helpers exposed to routes ──
    def get_all_raw(self) -> dict:
        return _load_db()

    def append_audit(self, action: str, entity: str, detail: str, performed_by: str = "admin"):
        _append_audit(action, entity, detail, performed_by)

    def get_audit_log(self):
        return _load_db().get("audit_log", [])

    def save_attendance_record(self, record: dict):
        """Save a daily attendance record (present/absent) for reporting."""
        data = _load_db()
        data.setdefault("attendance_log", []).append(record)
        _save_db(data)

    def mark_absent_students(self, date_str: str):
        """Mark all students who have no 'Today' timeline entry as Absent."""
        data = _load_db()
        students = data.get("students", [])
        absent_count = 0
        for student in students:
            timeline = student.get("timeline", [])
            has_today = any(e.get("day") == "Today" for e in timeline)
            if not has_today:
                # Add absent record
                timeline.append({
                    "day": "Today",
                    "emoji": "Absent",
                    "score": 0,
                    "alert": True,
                    "status": "absent",
                    "date": date_str
                })
                student["timeline"] = timeline
                student["risk"] = "Needs Attention"
                absent_count += 1
                # Log to attendance_log
                data.setdefault("attendance_log", []).append({
                    "roll_number": student.get("rollNumber"),
                    "name": f"{student.get('firstName')} {student.get('lastInitial')}",
                    "status": "absent",
                    "date": date_str
                })
        data["students"] = students
        _save_db(data)
        return absent_count


# Singleton
_db_instance = None

def get_database() -> PersistentDatabase:
    global _db_instance
    if _db_instance is None:
        _db_instance = PersistentDatabase()
    return _db_instance

async def connect_to_mongo():
    db = get_database()
    print(f"[DB] Persistent JSON database ready — {DB_FILE}")

async def close_mongo_connection():
    print("[DB] Database connection closed.")

# legacy alias
mock_db = None  # will be set lazily via get_database()
