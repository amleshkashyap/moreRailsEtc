import datetime
from singleton import Singleton

class VersionedKey():
    def __init__(self, key, timestamp):
        self.key = f"{key}@{timestamp}"
        return

class Storage():
    def __init__(self, storage_id):
        self.store = {}
        self.storage_id = storage_id
        return

    def put(self, versioned_key, value):
        self.store[versioned_key.key] = [value, str(datetime.datetime.utcnow())]
        return

    def get_store(self):
        return self.store

    def update_store(self, store):
        self.store = store
        return
