# needs cleanup
from server import Server
from client import Client
from system import SystemManager
from orders import Orders
from multiprocessing import Pool

def write(client):
    client.write()
    return

def ipc_write(conn, client):
    client.write()
    return


if __name__ == "__main__":
    # each distributed server updates a specific set of keys
    manager = SystemManager()
    orders = manager.orders
    multiproc_helper = manager.multiproc_helper
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    client = manager.get_new_client_system('distributed_client', manager.get_systems_of_type('distributed'))
    client.write()
    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: ", system.storage.store)
    print("\n****** Printing Orders **********")
    orders.print_orders()
    print("#########################")
    print("\n")


    # client communicates with leader-followers group, each group updates a specific set of keys
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('distributed_leader')
    manager.get_new_system('distributed_follower')
    manager.get_new_system('distributed_follower')
    manager.get_new_system('distributed_leader')
    manager.get_new_system('distributed_follower')
    manager.get_new_system('distributed_follower')
    client = manager.get_new_client_system('distributed_client', manager.get_systems_of_type('distributed_leader'))
    client.write()
    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed_leader') + manager.get_systems_of_type('distributed_follower'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: {system.storage.store}")
    print("\n****** Printing Orders **********")
    orders.print_orders()
    print("#########################")
    print("\n")


    # each distributed server updates a specific set of key, but 2 clients are communicating
    manager.reset_all_states()
    orders.reset_state()
    # each client has their own clock - only partial order is guaranteed, the true lamport clock scenario where some pairs are incomparable for the whole system
    client1 = manager.get_new_client_system('distributed_client', [manager.get_new_system('distributed')])
    client2 = manager.get_new_client_system('distributed_client', [manager.get_new_system('distributed')])
    client1.write()
    client2.write()
    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: {system.storage.store}")
    print("\n****** Printing Orders **********")
    orders.print_orders()
    print("#########################")
    print("\n")


    # simple leader follower servers with no lamport clock, just a global counter and a singleton storage
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('simple_leader')
    manager.get_new_system('simple_follower')
    manager.get_new_system('simple_follower')
    client = manager.get_new_client_system('simple_client', manager.get_systems_of_type('simple_leader'))
    client.write()
    client.write()
    print("Ouputs After Completion")
    for system in manager.get_systems_of_type('simple_leader') + manager.get_systems_of_type('simple_follower'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: {system.storage.store}")
    print("\n****** Printing Orders **********")
    orders.print_orders()
    print("\n")


    # each distributed server updates a specific set of keys - but the operations are separate threads now, being fired in unknown ordering
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    all_clients = []
    print("Creating Clients For Multithreaded Execution")
    # when using a larger value, tabulation won't show its benefits - need logging
    for i in range(2):
        all_clients.append(manager.get_new_client_system('distributed_client', manager.get_systems_of_type('distributed')))

    tasks = [(c.write()) for c in all_clients]
    future = multiproc_helper.__class__.submit_tasks_to_thread_pool_synchronously(tasks)

    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: ", system.storage.store)
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
    print("#########################")


    # each distributed server updates a specific set of keys - but the operations are separate processes now, without shared memory - this doesn't work
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    all_clients = []
    print("Creating Clients For Multiprocess Execution")
    for i in range(2):
        all_clients.append(manager.get_new_client_system('distributed_client', manager.get_systems_of_type('distributed')))

    multiproc_helper.__class__.submit_tasks_to_process_pool_synchronously(write, all_clients)

    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: ", system.storage.store)
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
    print("#########################")


    # each distributed server updates a specific set of keys - but the operations are separate processes now, with message passing - output is similar to multithreaded case
    manager.reset_all_states()
    orders.reset_state()
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    manager.get_new_system('distributed')
    print("Creating Clients For Multiprocess Execution With IPC")
    parent_conn1, child_conn1 = multiproc_helper.__class__.get_pipe()
    parent_conn2, child_conn2 = multiproc_helper.__class__.get_pipe()
    client1 = manager.get_new_communicating_client_system('communicating_client', child_conn1, manager.get_systems_of_type('distributed'))
    client2 = manager.get_new_communicating_client_system('communicating_client', child_conn2, manager.get_systems_of_type('distributed'))

    p1 = multiproc_helper.__class__.get_process(ipc_write, (child_conn1, client1))
    p2 = multiproc_helper.__class__.get_process(ipc_write, (child_conn2, client2))
    p1.start()
    p2.start()
    children_finished = 0
    while(children_finished < 2):
        msgs = { 0: parent_conn1.recv(), 1: parent_conn2.recv() }
        for k, msg in msgs.items():
            if k == 0:
                p_conn = parent_conn1
                c_conn = child_conn1
                client = client1
            else:
                p_conn = parent_conn2
                c_conn = child_conn2
                client = client2

            if msg[0] == "add_order":
                client.orders.add_order(msg[1], msg[2], msg[3])
            elif msg[0] == "server_write":
                s = manager.get_system_by_id(msg[1])
                w = s.write(msg[2], msg[3], msg[4])
                p_conn.send(w)
            elif msg[0] == "close_connection":
                c_conn.close()
                children_finished += 1

    p1.join()
    p2.join()

    print("Outputs After Completion")
    for system in manager.get_systems_of_type('distributed'):
        print(f"    Server Type {system.system_type}, Server-{system.system_id} Storage: ", system.storage.store)
    print("****** Printing Orders **********")
    orders.print_orders()
    print("\n")
    print("#########################")
