import time
from singleton import Singleton
from multiprocessing import Process, Manager, Lock, Pipe, TimeoutError, Pool, Queue
from concurrent.futures import ThreadPoolExecutor
MAX_THREAD_POOL_SIZE = 5
MAX_PROCESS_POOL_SIZE = 5

class MultiProcessHelper(Singleton):
    def __init__(self):
        return

    @staticmethod
    def submit_tasks_to_thread_pool_synchronously(tasks):
        future = ThreadPoolExecutor(MAX_THREAD_POOL_SIZE).submit(tasks, ('Completed'))
        while future.done == False:
            print(future.done)
            time.sleep(1)
            continue
        return future

    @staticmethod
    def submit_tasks_to_process_pool_synchronously(function, arguments):
        with Pool(MAX_PROCESS_POOL_SIZE) as p:
            p.map(function, arguments)
        return

    @staticmethod
    def get_pipe():
        return Pipe()

    @staticmethod
    def get_process(target, arguments):
        return Process(target=target, args=arguments)

    def spawn_process_with_join(self, target, arguments, timeout=None, lock=None):
        p = Process(target=target, args=arguments)
        p.start()
        p.join()
        return p.get()
