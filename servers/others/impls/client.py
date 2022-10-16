from singleton import Singleton
from lamport_clock import LamportClock, MonotonicClock

class Client():
    def __init__(self, system_id, system_type, servers, orders):
        self.clock = LamportClock(1)
        self.system_type = system_type
        self.servers = servers
        self.system_id = system_id
        self.orders = orders
        print(f"Created System Of Type {system_type}, With ID: {system_id}")
        self.orders.add_order(self.clock.get_latest_time(), system_id, "created")
        return

    def add_server_to_request(self, server):
        self.servers.append(server)
        return

    def write(self):
        server_write_at = []
        for server in self.servers:
            self.orders.add_order(self.clock.get_latest_time(), self.system_id, f"making_request_to_{server.system_id}")
            if "_follower" in server.system_type or server.system_type == 'simple':
                continue
            write_at = server.write(f"key-{server.system_id}", f"value-{server.system_id}", self.clock.get_latest_time())
            server_write_at.append(write_at)
            self.clock.set_latest_time(write_at)
            self.orders.add_order(self.clock.get_latest_time(), self.system_id, f"completed_request_to_{server.system_id}")
            print(f"    Server-{server.system_id}: {write_at}")

        assert server_write_at == sorted(server_write_at)
        return
