from singleton import Singleton
from storage import Storage
from server import Server
from client import Client, IPCClient
from process import Process
from orders import Orders
from multiprocs import MultiProcessHelper

class SystemManager(Singleton):
    def __init__(self):
        self.orders = Orders()
        self.multiproc_helper = MultiProcessHelper()
        self.systems = AllSystems()
        self.storages = AllStorages()
        self.global_store = self.storages.get_storage(0)
        self.processes = AllProcesses()
        pass

    def reset_all_states(self):
        self.systems.reset_state()
        self.storages.reset_state()
        self.global_store.reset_state()
        self.processes.reset_state()

    def get_new_client_system(self, s_type, servers=[]):
        return self.systems.add_client_system(s_type, servers, self.orders, None)

    def get_new_communicating_client_system(self, s_type, connection, servers=[]):
        return self.systems.add_communicating_client_system(s_type, servers, self.orders, connection)

    def get_new_system(self, s_type):
        return self.systems.add_system(s_type, self.orders, self.multiproc_helper)

    def get_system_by_id(self, s_id):
        return self.systems.get_system(s_id)

    def get_systems_of_type(self, system_type):
        return self.systems.get_systems_of_type(system_type)

    def get_new_storage(self, storage_type):
        return self.storages.add_storage(storage_type)

    def get_storage_by_id(self, storage_id):
        return self.storages.get_storage(storage_id)

    def get_new_process(self, process_type, system_id):
        return self.processes.add_process(process_type, system_id)

    def get_process_by_id(self, process_id):
        return self.processes.get_process(process_id)


class AllProcesses(Singleton):
    def __init__(self):
        self.count = {}
        self.all_processes = {}
        return

    def add_process(self, process_type, system_id):
        c = self.count.get(system_id)
        if isinstance(c, int):
            c += 1
        else:
            c = 0
        self.count[system_id] = c
        process = Process(c, process_type, system_id)
        p = self.all_processes.get(system_id)
        if isinstance(self.all_processes[system_id], list):
            self.all_processes.append(process)
        else:
            self.all_processes = [process]
        return process

    def get_process_by_system_and_id(self, p_id, system_id):
        return self.all_processes[system_id][p_id]

    def reset_state(self):
        self.count = {}
        self.all_processes = {}
        return


class SingletonStorage(Storage, Singleton):
    def __init__(self):
        super().__init__(0)
        return

    def reset_state(self):
        self.store = []
        return


class AllStorages():
    def __init__(self):
        self.all_storages = [SingletonStorage()]
        self.count = 0
        return

    def add_storage(self, storage_type):
        self.count += 1
        storage = Storage(self.count, storage_type)
        self.all_storages.append(storage)
        return storage

    def get_storage(self, storage_id):
        return self.all_storages[storage_id]

    def reset_state(self):
        singleton_store = self.all_storages[0]
        singleton_store.reset_state()
        self.all_storages = [singleton_store]
        self.count = 0
        return


class AllSystems(Singleton):
    def __init__(self):
        self.all_systems = []
        self.count = -1

    def add_system(self, s_type, orders, multiproc_helper):
        self.count += 1
        if s_type in ['simple_client', 'distributed_client']:
            system = Client(self.count, s_type, [], orders, None)
        elif s_type == 'communicating_client':
            system = IPCClient(self.count, s_type, [], orders, None)
        else:
            leader_id = self.get_last_leader(s_type)
            system = Server(self.count, s_type, leader_id, orders, multiproc_helper)
            if "_follower" in s_type:
                leader = self.get_system(leader_id)
                leader.update_followers(self.count)
                system.update_storage(leader.get_storage())
        self.all_systems.append(system)
        return system

    def add_client_system(self, s_type, servers, orders, multiproc_helper):
        self.count += 1
        system = Client(self.count, s_type, servers, orders, None)
        self.all_systems.append(system)
        return system

    def add_communicating_client_system(self, s_type, servers, orders, connection):
        self.count += 1
        system = IPCClient(self.count, s_type, servers, orders, connection)
        self.all_systems.append(system)
        return system

    def get_system(self, system_id):
        return self.all_systems[system_id]

    def get_systems_of_type(self, system_type):
        systems = [ s for s in self.all_systems if s.system_type == system_type ]
        return systems

    def get_last_leader(self, system_type):
        if "_follower" not in system_type:
            return None
        s_type_prefix = system_type.split("_")[0]
        lead_system_type = f"{s_type_prefix}_leader"
        leader_ids = [t.system_id for t in self.all_systems if t.system_type == lead_system_type]
        if len(leader_ids) == 0:
            raise RuntimeError(f"Follower server was created in an invalid order, create a leader server first")
        return leader_ids[-1]

    def update_follower_storage(self, system_id):
        follower_servers = [t for t in self.all_systems if t.leader_id == system_id]
        for server in follower_servers:
            server.write(None, None, None)
        return

    def reset_state(self):
        self.count = -1
        # this doesn't work
        for system in self.all_systems:
            if '_leader' in system.system_type:
                del system.storage
            del system
        self.all_systems = []
        return
