import asyncio

class MockCursor:
    def __init__(self, data):
        self.data = data
    async def to_list(self, length=1000):
        return self.data[:length]

class MockResult:
    def __init__(self, inserted_id=None, matched_count=0):
        self.inserted_id = inserted_id
        self.matched_count = matched_count

class MockCollection:
    def __init__(self):
        self.documents = []
        self._id_counter = 1

    def find(self, query=None):
        if not query:
            return MockCursor(list(self.documents))
        results = []
        for doc in self.documents:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                results.append(doc)
        return MockCursor(results)

    async def find_one(self, query):
        for doc in self.documents:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return dict(doc)
        return None

    async def insert_one(self, document):
        doc = dict(document)
        doc["_id"] = str(self._id_counter)
        self._id_counter += 1
        self.documents.append(doc)
        return MockResult(inserted_id=doc["_id"])

    async def update_one(self, query, update, upsert=False):
        doc = await self.find_one(query)
        if doc:
            index = next(i for i, d in enumerate(self.documents) if d["_id"] == doc["_id"])
            target = self.documents[index]
            
            if "$set" in update:
                target.update(update["$set"])
            if "$push" in update:
                for k, v in update["$push"].items():
                    if k not in target:
                        target[k] = []
                    target[k].append(v)
            return MockResult(matched_count=1)
        elif upsert:
            new_doc = dict(query)
            if "$set" in update:
                new_doc.update(update["$set"])
            await self.insert_one(new_doc)
            return MockResult(matched_count=1)
        return MockResult(matched_count=0)

class MockDatabase:
    def __init__(self):
        self.students = MockCollection()
        # Seed some data for the dashboard
        asyncio.run(self.students.insert_one({
            "firstName": "Arnab",
            "lastInitial": "S",
            "rollNumber": "182",
            "class": "Nursery-A",
            "attendance": 100,
            "risk": "Stable",
            "parentStatus": "Pending",
            "timeline": []
        }))

mock_db = MockDatabase()

async def connect_to_mongo():
    print("Using Mock MongoDB due to Atlas connection timeout!")

async def close_mongo_connection():
    print("Closed Mock MongoDB connection.")

def get_database():
    return mock_db
