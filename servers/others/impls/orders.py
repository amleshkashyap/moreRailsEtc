from singleton import Singleton
from tabulate import tabulate

class Orders(Singleton):
    def __init__(self):
        self.total_order = []
        self.clock_server_values = {}
        return

    def add_order(self, timestamp, system_id, event_name):
        v = self.clock_server_values.get(timestamp)
        if v == None:
            self.clock_server_values.update({ timestamp: { system_id: [event_name] } })
        else:
            s = v.get(system_id)
            if s == None:
                self.clock_server_values[timestamp].update({ system_id: [event_name] })
            else:
                s.append(event_name)
                self.clock_server_values[timestamp].update({ system_id: s })
        return

    def reset_state(self):
        self.total_order = []
        self.clock_server_values = {}
        return

    def print_orders(self):
        all_systems = []
        all_timestamps = sorted(self.clock_server_values.keys())
        for k, v in self.clock_server_values.items():
            for i, j in v.items():
                all_systems.append(i)

        all_systems = sorted(list(dict.fromkeys(all_systems)))
        all_systems = ["Clocks/Servers"] + all_systems
        idx = 0
        for k, v in self.clock_server_values.items():
            self.total_order.append(len(all_systems) * [None])
            self.total_order[idx][0] = k
            for i, j in v.items():
                self.total_order[idx][all_systems.index(i)] = j
            idx += 1
        print(tabulate(self.total_order, all_systems, tablefmt='fancy_grid'))
        return
