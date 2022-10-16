# needs cleanup
from server import Server
from client import Client
from system import SystemManager
from orders import Orders

if __name__ == "__main__":
    # each distributed server updates a specific set of keys
    manager = SystemManager()
    orders = manager.orders
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    client = manager.get_new_client_system('client', manager.get_systems_of_type('distributed'))
    client.write()
    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: ", system.storage.store)
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
    print("#########################")

    # client communicates with leader-followers group, each group updates a specific set of keys
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('distributed_leader')
    manager.get_new_system('distributed_follower')
    manager.get_new_system('distributed_follower')
    manager.get_new_system('distributed_leader')
    manager.get_new_system('distributed_follower')
    manager.get_new_system('distributed_follower')
    client = manager.get_new_client_system('client', manager.get_systems_of_type('distributed_leader'))
    client.write()
    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed_leader') + manager.get_systems_of_type('distributed_follower'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: {system.storage.store}")
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
    print("#########################")

    # each distributed server updates a specific set of key, but 2 clients are communicating
    manager.reset_all_states()
    orders.reset_state()
    # each client has their own clock - only partial order is guaranteed, the true lamport clock scenario where some pairs are incomparable for the whole system
    client1 = manager.get_new_client_system('client', [manager.get_new_system('distributed')])
    client2 = manager.get_new_client_system('client', [manager.get_new_system('distributed')])
    client1.write()
    client2.write()
    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: {system.storage.store}")
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
    print("#########################")

    # simple leader follower servers with no lamport clock, just a global counter and a singleton storage
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('simple_leader')
    manager.get_new_system('simple_follower')
    manager.get_new_system('simple_follower')
    client = manager.get_new_client_system('client', manager.get_systems_of_type('simple_leader'))
    client.write()
    client.write()
    print("Ouputs After Completion")
    for system in manager.get_systems_of_type('simple_leader') + manager.get_systems_of_type('simple_follower'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: {system.storage.store}")
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
