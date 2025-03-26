""" Thread pool implementation """
import os
import json
from queue import Queue
from threading import Thread, Event
import multiprocessing
import logging
from typing import Optional, Any


class ThreadPool:
    """ Thread pool implementation """

    def __init__(self):
        self.job_queue = Queue()
        self.shutdown_event = Event()
        self.num_threads = int(os.getenv('TP_NUM_OF_THREADS', multiprocessing.cpu_count()))
        self.runners = [
            TaskRunner(self.job_queue, self.shutdown_event)
            for _ in range(self.num_threads)
        ]

        # Ensure results directory exists
        os.makedirs('results', exist_ok=True)

        for runner in self.runners:
            runner.start()

    def add_task(self, job_id: str, task_func, *args, **kwargs):
        """ Add a task to the queue """
        self.job_queue.put((job_id, task_func, args, kwargs))

    def graceful_shutdown(self):
        """Gracefully shutdown the thread pool"""
        self.shutdown_event.set()
        for runner in self.runners:
            runner.join()

    def is_job_done(self, job_id: str) -> bool:
        """ Check if a job is done """
        return os.path.exists(f'results/{job_id}.json')

    def get_job_result(self, job_id: str) -> Optional[Any]:
        """ Get the result of a job """
        try:
            with open(f'results/{job_id}.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None


class TaskRunner(Thread):
    """ Task runner thread """

    def __init__(self, job_queue: Queue, shutdown_event: Event):
        super().__init__(daemon=True)
        self.job_queue = job_queue
        self.shutdown_event = shutdown_event
        self.logger = logging.getLogger('webserver')

    def run(self):
        while not self.shutdown_event.is_set():
            job_id, task_func, args, kwargs = self.job_queue.get(timeout=1)
            self._process_job(job_id, task_func, args, kwargs)

    def _process_job(self, job_id: str, task_func, args, kwargs):
        """Process an individual job with error handling"""
        try:
            self.logger.info(f'Starting job {job_id}')
            result = task_func(*args, **kwargs)

            with open(f'results/{job_id}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f)

            self.logger.info(f'Completed job {job_id}')
        except Exception as e:
            self.logger.error(f'Error in job {job_id}: {str(e)}')
            with open(f'results/{job_id}.json', 'w', encoding='utf-8') as f:
                json.dump({'status': 'error', 'reason': str(e)}, f)
        finally:
            self.job_queue.task_done()
