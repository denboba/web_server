""" Thread pool implementation """
import os
import json
from queue import Queue, Empty
from threading import Thread, Event
import multiprocessing
import logging
from typing import Optional, Any


class ThreadPool:
    """ Thread pool implementation """

    def __init__(self):
        self.logger = logging.getLogger('webserver')
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
        return (os.path.exists(f'results/{job_id}.json') and
                os.path.getsize(f'results/{job_id}.json') > 0)

    def get_job_result(self, job_id: str) -> Optional[Any]:
        """ Get the result of a completed job """
        file_path = f'results/{job_id}.json'
        try:
            if not os.path.exists(file_path):
                self.logger.error('File %s does not exist', file_path)
            if os.path.getsize(file_path) == 0:
                self.logger.error("Job result file is empty: %s", file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error("Failed to decode JSON from file %s: %s",
                              file_path, str(e))
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
            try:
                job_id, task_func, args, kwargs = self.job_queue.get(timeout=1)
                self._process_job(job_id, task_func, args, kwargs)
            except Empty:
                continue
            except (KeyError, TypeError, ValueError) as e:
                self.logger.error('Runner error: %s: %s', type(e).__name__, str(e))

    def _process_job(self, job_id: str, task_func, args, kwargs):
        """Process an individual job with error handling"""
        try:
            self.logger.info('Starting job %s', job_id)
            result = task_func(*args, **kwargs)

            with open(f'results/{job_id}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f)

            self.logger.info('Completed job %s', job_id)
        except FileNotFoundError as e:
            self.logger.error('File not found error in job %s: %s', job_id, str(e))
            with open(f'results/{job_id}.json', 'w', encoding='utf-8') as f:
                json.dump({'status': 'error', 'reason': 'File not found error: ' + str(e)}, f)
        except OSError as e:
            self.logger.error('OS error in job %s: %s', job_id, str(e))
            with open(f'results/{job_id}.json', 'w', encoding='utf-8') as f:
                json.dump({'status': 'error', 'reason': 'OS error: ' + str(e)}, f)
        finally:
            self.job_queue.task_done()
