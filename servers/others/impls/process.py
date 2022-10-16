import datetime
from singleton import Singleton

class Process():
    def __init__(self, process_id, process_type, system_id):
        self.process_id = process_id
        self.process_type = process_type
        self.state = 'new'
        self.invocation_timestamp = str(datetime.datetime.utcnow())
        self.system_id = system_id
        return

    def start_process(self):
        self.state = 'running'
        self.start_timestamp = str(datetime.datetime.utcnow())
        return

    def kill_process(self):
        self.state = 'killed'
        self.end_timestamp = str(datetime.datetime.utcnow())
        return

    def get_state(self):
        return self.state
