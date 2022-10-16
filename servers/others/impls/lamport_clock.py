from singleton import Singleton

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


class MonotonicClock(LamportClock):
    def __init__(self):
        super().__init__(0)
        return

    def tick(self):
        self.set_latest_time(self.latest_time + 1)
        return self.latest_time

class Clock(LamportClock):
    def __init__(self):
        super().__init__(0)
        return

    def tick(self):
        pass
