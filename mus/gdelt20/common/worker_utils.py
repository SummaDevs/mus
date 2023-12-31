from multiprocessing import cpu_count
from queue import Queue
from threading import Lock
from threading import Thread

CONCURRENCY_NUM_MIN = 4
CONCURRENCY_NUM_MAX = 12

CONCURENCY_NUM = max(
    CONCURRENCY_NUM_MIN,
    min(cpu_count() * 2, CONCURRENCY_NUM_MAX)
)

LOCK_OBJ = Lock()


class JobQueue(object):
    def __init__(self):
        """
        Initiate
        """
        self.queue = Queue()
        self.lock = Lock()

    def put(self, item):
        """
        Puts worker's  parameters

        :param item: item to process
        """
        self.queue.put(item)

    def get(self):
        """
        Get worker's  parameters

        """
        return self.queue.get()

    def start(self, concurrency, worker, **kwargs):
        """
        Start workers

        :param concurrency: number of threads
        :param worker: callable
        :param kwargs: arguments to pass into workers
        """
        kwargs["queue"] = self
        for worker_num in range(concurrency):
            dargs = kwargs.copy()
            dargs["worker_num"] = worker_num

            w = Thread(target=worker, kwargs=dargs, daemon=True)
            w.start()

        self.queue.join()

    def task_done(self):
        """
        Indicate that a formerly enqueued task is complete.
        """
        self.queue.task_done()

    def lock_flush(self):
        """
        Force safe working queue clearance
        Note: queue.full does not work
        """
        with self.lock:
            while not self.queue.empty():
                self.queue.get()
                self.queue.task_done()
