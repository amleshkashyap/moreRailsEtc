from singleton import Singleton
from lamport_clock import LamportClock, MonotonicClock, Clock
from storage import Storage, VersionedKey
from orders import Orders

class Server():
    def __init__(self, system_id, system_type, leader_id, orders, storage_id=None):
        self.is_leader = False
        self.system_type = system_type
        self.system_id = system_id
        self.leader_id = leader_id
        self.follower_ids = []
        self.orders = orders

        if system_type == 'simple':
            self.clock = MonotonicClock()
            self.storage = SingletonStorage()
        elif system_type == 'simple_leader':
            self.clock = MonotonicClock()
            self.storage = Storage(system_id)
            self.is_leader = True
        elif system_type == 'simple_follower':
            self.clock = Clock()
            self.storage = None

        elif system_type == 'distributed':
            self.clock = LamportClock(1)
            self.storage = Storage(system_id)
        elif system_type == 'distributed_leader':
            self.clock = LamportClock(1)
            self.storage = Storage(system_id)
            self.is_leader = True
        elif system_type == 'distributed_follower':
            self.clock = Clock()
            self.storage = None
        else:
            raise RuntimeError(f"Invalid Server Type: {system_type}")

        print(f"Created System Of Type {system_type}, With ID {self.system_id}")
        self.orders.add_order(self.clock.get_latest_time(), system_id, "created")
        # python has this problem of considering 0 as False
        if self.leader_id != None:
            print(f"    Lead Server Is: {self.leader_id}")
        return

    def update_followers(self, follower_id):
        self.follower_ids.append(follower_id)
        return

    def get_storage(self):
        return self.storage

    def update_storage(self, storage):
        self.storage = storage
        return

    def write(self, key, value, timestamp):
        write_at = None
        if self.system_type == 'simple':
            write_at = self.clock.tick()
            self.storage.put(VersionedKey(key, write_at), value)

        elif self.system_type == 'simple_leader':
            write_at = self.clock.tick()
            self.storage.put(VersionedKey(key, write_at), value)
            # AllServers.update_follower_storage(self.system_id)

        elif self.system_type == 'simple_follower':
            # self.storage = AllServers.get_server(self.leader_id).storage
            pass

        elif self.system_type == 'distributed':
            write_at = self.clock.tick(timestamp)
            self.storage.put(VersionedKey(key, write_at), value)
            self.orders.add_order(self.clock.get_latest_time(), self.system_id, f"written_{key}")

        elif self.system_type == 'distributed_leader':
            write_at = self.clock.tick(timestamp)
            self.storage.put(VersionedKey(key, write_at), value)
            self.orders.add_order(self.clock.get_latest_time(), self.system_id, f"written_{key}")
            # AllServers.update_follower_storage(self.system_id)

        elif self.system_type == 'distributed_follower':
            # self.storage = AllServers.get_server(self.leader_id).storage
            pass

        return write_at
