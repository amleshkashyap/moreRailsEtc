from singleton import Singleton
from lamport_clock import LamportClock, MonotonicClock

class Client():
    def __init__(self, system_id, system_type, servers, orders, multiproc_helper):
        if system_type == 'distributed_client':
            self.clock = LamportClock(1)
        else:
            self.clock = MonotonicClock(1)
        self.system_type = system_type
        self.servers = servers
        self.system_id = system_id
        self.orders = orders
        self.multiproc_helper = multiproc_helper
        # print(f"Created System Of Type {system_type}, With ID: {system_id}")
        self.orders.add_order(self.clock.get_latest_time(), system_id, "created")
        return

    def add_server_to_request(self, server):
        self.servers.append(server)
        return

    def write(self):
        server_write_at = []
        for server in self.servers:
            if "_follower" in server.system_type or server.system_type == 'simple':
                continue
            timestamp = self.clock.get_latest_time()
            key = f"key-s{server.system_id}-c{self.system_id}-{timestamp}"
            value = f"value-s{server.system_id}-c{self.system_id}-{timestamp}"
            print(f"Sending {key}")
            self.orders.add_order(timestamp, self.system_id, f"init_{server.system_id}_w_{key}")
            write_at = server.write(key, value, timestamp)
            server_write_at.append(write_at)
            self.clock.set_latest_time(write_at)
            self.orders.add_order(self.clock.get_latest_time(), self.system_id, f"done_{server.system_id}_w_{key}")

        assert server_write_at == sorted(server_write_at)
        return

class IPCClient(Client):
    def __init__(self, system_id, system_type, servers, orders, connection):
        super().__init__(system_id, 'distributed_client', servers, orders, None)
        self.system_type = system_type
        self.connection = connection

    def write(self):
        server_write_at = []
        for server in self.servers:
            if "_follower" in server.system_type or server.system_type == 'simple':
                continue
            timestamp = self.clock.get_latest_time()
            key = f"key-s{server.system_id}-c{self.system_id}-{timestamp}"
            value = f"value-s{server.system_id}-c{self.system_id}-{timestamp}"
            self.connection.send(["add_order", timestamp, self.system_id, f"init_{server.system_id}_w_{key}"])
            self.connection.send(["server_write", server.system_id, key, value, timestamp])
            write_at = self.connection.recv()
            server_write_at.append(write_at)
            self.clock.set_latest_time(write_at)
            self.connection.send(["add_order", self.clock.get_latest_time(), self.system_id, f"done_{server.system_id}_w_{key}"])

        self.connection.send(["close_connection"])
        assert server_write_at == sorted(server_write_at)
        return
