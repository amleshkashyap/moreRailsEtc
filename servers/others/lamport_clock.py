# needs cleanup
import datetime

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AllServers():
    all_servers = []
    server_count = -1

    @staticmethod
    def get_server_id():
        AllServers.server_count += 1
        return AllServers.server_count

    @staticmethod
    def add_server(server, server_id):
        if AllServers.server_count != server_id:
            raise RuntimeError(f"Invalid Server Being Added: Given ID - {server_id}, Expected ID - {count}")
        AllServers.all_servers.append(server)
        return

    @staticmethod
    def get_server(server_id):
        return AllServers.all_servers[server_id]

    @staticmethod
    def get_last_leader(server_type):
        leader_ids = [t.server_id for t in AllServers.all_servers if t.server_type == server_type]
        return leader_ids[-1]

    @staticmethod
    def update_follower_storage(server_id):
        follower_servers = [t for t in AllServers.all_servers if t.leader_id == server_id]
        for server in follower_servers:
            server.write(None, None, None)
        return

    @staticmethod
    def reset_all_states():
        AllServers.server_count = -1
        # this doesn't work
        for server in AllServers.all_servers:
            if '_leader' in server.server_type:
                del server.storage
            del server
        AllServers.all_servers = []
        SingletonStorage().store = {}


class LamportClock():
    def __init__(self, timestamp):
        self.latest_time = timestamp
        return

    # server should call this method at every action with 'timestamp' coming from client
    # return the new timestamp back to the client so that client has an updated value for future requests to the server to maintain partial ordering
    def tick(self, timestamp):
        self.latest_time = max(timestamp, self.latest_time)
        self.latest_time += 1
        return self.latest_time

    def get_latest_time(self):
        return self.latest_time

    def set_latest_time(self, timestamp):
        self.latest_time = timestamp
        return


class GlobalCounter():
    def __init__(self):
        self.counter = 0
        return

    def tick(self):
        self.counter += 1
        return self.counter


class VersionedKey():
    def __init__(self, key, timestamp):
        self.key = f"{key}@{timestamp}"
        return


class Storage():
    def __init__(self):
        self.store = {}
        return

    def put(self, versioned_key, value):
        self.store[versioned_key.key] = [value, str(datetime.datetime.utcnow())]
        return


class SingletonStorage(Storage, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        return


class Server():
    def __init__(self, server_type='simple'):
        self.is_leader = False
        self.server_type = server_type
        self.leader_id = None

        if server_type == 'simple':
            self.storage = SingletonStorage()
        elif server_type == 'simple_leader':
            self.counter = GlobalCounter()
            self.storage = Storage()
            self.is_leader = True
        elif server_type == 'simple_follower':
            self.storage = None
            self.leader_id = AllServers.get_last_leader('simple_leader')

        elif server_type == 'distributed':
            self.clock = LamportClock(1)
            self.storage = Storage()
        elif server_type == 'distributed_leader':
            self.clock = LamportClock(1)
            self.storage = Storage()
            self.is_leader = True
        elif server_type == 'distributed_follower':
            self.storage = None
            self.leader_id = AllServers.get_last_leader('distributed_leader')
        else:
            raise RuntimeError(f"Invalid Server Type: {server_type}")

        self.server_id = AllServers.get_server_id()
        AllServers.add_server(self, self.server_id)
        print(f"Created Server Of Type {server_type}, With ID {self.server_id}")
        # python has this problem of considering 0 as False
        if self.leader_id != None:
            print(f"    Lead Server Is: {self.leader_id}")
        return

    def write(self, key, value, timestamp):
        write_at = None
        if self.server_type == 'simple':
            write_at = self.counter.tick()
            self.storage.put(VersionedKey(key, write_at), value)

        elif self.server_type == 'simple_leader':
            write_at = self.counter.tick()
            self.storage.put(VersionedKey(key, write_at), value)
            AllServers.update_follower_storage(self.server_id)

        elif self.server_type == 'simple_follower':
            self.storage = AllServers.get_server(self.leader_id).storage


        elif self.server_type == 'distributed':
            write_at = self.clock.tick(timestamp)
            self.storage.put(VersionedKey(key, write_at), value)
            
        elif self.server_type == 'distributed_leader':
            write_at = self.clock.tick(timestamp)
            self.storage.put(VersionedKey(key, write_at), value)
            AllServers.update_follower_storage(self.server_id)

        elif self.server_type == 'distributed_follower':
            self.storage = AllServers.get_server(self.leader_id).storage

        return write_at

class Client():
    def __init__(self, servers):
        self.clock = LamportClock(1)
        self.servers = servers
        return

    def write(self):
        server_write_at = []
        for server in self.servers:
            if "_follower" in server.server_type or server.server_type == 'simple':
                continue
            write_at = server.write(f"key-{server.server_id}", f"value-{server.server_id}", self.clock.get_latest_time())
            server_write_at.append(write_at)
            self.clock.set_latest_time(write_at)
            print(f"Server-{server.server_id}: {write_at}")

        assert server_write_at == sorted(server_write_at)
        return


if __name__ == "__main__":
    # each distributed server updates a specific set of keys
    Server('distributed')
    Server('distributed')
    Server('distributed')
    client = Client(AllServers.all_servers)
    client.write()
    print("\n")
    for server in AllServers.all_servers:
        print(f"Server Type {server.server_type}, Server-{server.server_id} Storage: ", server.storage.store)
    print("#########################")
    print("\n")

    # client communicates with leader-followers group, each group updates a specific set of keys
    AllServers.reset_all_states()
    Server('distributed_leader')
    Server('distributed_follower')
    Server('distributed_follower')
    Server('distributed_leader')
    Server('distributed_follower')
    Server('distributed_follower')
    client = Client(AllServers.all_servers)
    client.write()
    print("\n")
    for server in AllServers.all_servers:
        print(f"Server Type {server.server_type}, Server-{server.server_id} Storage: {server.storage.store}")
    print("#########################")
    print("\n")

    # each distributed server updates a specific set of key, but 2 clients are communicating
    AllServers.reset_all_states()
    client1 = Client([Server('distributed')])
    client2 = Client([Server('distributed')])
    client1.write()
    client2.write()
    print("\n")
    for server in AllServers.all_servers:
        print(f"Server Type {server.server_type}, Server-{server.server_id} Storage: {server.storage.store}")
    print("#########################")
    print("\n")

    # simple leader follower servers with no lamport clock, just a global counter and a singleton storage
    AllServers.reset_all_states()
    Server('simple_leader')
    Server('simple_follower')
    Server('simple_follower')
    client = Client(AllServers.all_servers)
    client.write()
    client.write()
    print("\n")
    for server in AllServers.all_servers:
        print(f"Simple Server Type {server.server_type}, Server-{server.server_id} Storage: {server.storage.store}")
