# Health_Data_Webserver(le-stats-sportif)
## Name: Abdulkadir Gobena DENBOBA
## Group: 332CC

## Assignment TODO

A health data analytics server which analyzes obesity, nutrition, and physical inactivity data over the states in the US. The server offers statistical analysis via REST API endpoints, and processes requests through a thread pool.

## Organization
```
├── app/
│   ├── __init__.py         # Main module initializer
│   ├── data_ingestor.py    # Data analysis
│   ├── routes.py           # API endpoints
│   └── task_runner.py      # Thread handling
├── unittests/
│   └── mytests.py          # Unit tests for data_ingestor.py
├── requirements.txt       # Dependencies
├── webserver.log           # Log file
└── nutrition_activity_obesity_usa_subset.csv # Input data


```
## Solution Explanation


#### General Approach

This solution implements a thread pool to serve multiple incoming requests. For every request received:

1. A new job ID is created
2. A free worker thread will handle the job
3. The job will be stored under results/job_id_x.json where x is the job ID
```python
def get_next_job_id():
    """this function returns the next job id"""
    job_id = f"job_id_{webserver.job_counter}"
    webserver.job_counter += 1
    return job_id
```
Some of the core processing logic looks like this:

```python
class ThreadPool:
    def __init__(self):
        self.job_queue = Queue()
        self.shutdown_event = Event()
        self.num_threads = multiprocessing.cpu_count()
        self.runners = [
            TaskRunner(self.job_queue, self.shutdown_event)
            for _ in range(self.num_threads)
        ]
```

#### Assignment Usefulness

this assignment is useful because it covers the following topics:
- Practical concurrent programming
- Real-world data processing problems using pandas
- API design principles
- The importance of thread synchronization is demonstrated
- implementation of high quality python code with unit tests and pylint
- Flask Framework
- modular design and separation of concerns
#### Implementation

- The implementation uses an Efficient thread pool because it scales with the number of CPU cores 
- The ThreadPool abd TaskRunner classes are implemented  to handle concurrent requests without race conditions
- The DataIngestor class is implemented in a way that it is thread-safe using the ThreadPool and pandas
- The functionality of DataIngestor methods is tested using unittests using the test input and output files
- logging is logged to a file to webserver.log with sufficient detail

#### data_ingestor.py
- deals mainly with data ingestion and processing being helper for the functions from routes.py
- it is thread-safe using the ThreadPool and pandas
- is tested using unittests using the tests directory input and output files
- it is also responsible for loading the CSV file into a pandas DataFrame

#### routes.py 
- contains the endpoints for the API
- it is responsible for handling the request by calling the appropriate methods from data_ingestor.py

#### task_runner.py
- deals with thread handling and job execution
- it is responsible for processing the jobs in a non-blocking manner
- it is implemented thread safely using Event and Queue and necessary methods

#### unittests/mytests.py
- it is responsible for testing the functionality of the methods in data_ingestor.py which are used for extracting data from the CSV file and processing it
### Completeness

All the necessary tasks have been implemented without losing functionality. They include:
- Statistical processes REST endpoints
- Asynchronous job execution
- Job control
- Thread safety

### Extra Features
1. Dynamic thread pool
   - Ability to dynamically adjust the number of threads based on the available system resources

### Missing Features
None. All required features are implemented and covered by tests.

### Challenges

Processing data issues:
- Synchronization issues: checking if a job is done and getting the result
- Package-Level Modality Issues: importing the packages and CSV value correctly inside the two package app and unittests:
- cyclic imports from skeleton code
```python
PYLINT OUTPUT
>>>>>>
************* Module app
app/__init__.py:36:0: C0413: Import "from app import routes" should be placed at the top of the module (wrong-import-position)
************* Module app.routes
app/routes.py:277:8: R1713: Consider using str.join(sequence) for concatenating strings from an iterable (consider-using-join)
app/routes.py:1:0: R0401: Cyclic import (app -> app.routes) (cyclic-import)

```
### solution
``` python
 def is_job_done(self, job_id: str) -> bool:
        """ Check if a job is done """
        return os.path.exists(f'results/{job_id}.json') and os.path.getsize(f'results/{job_id}.json') > 0
```
- 
``` python

logger.info('Thread pool initialized')
LOCAL_FILE = "./nutrition_activity_obesity_usa_subset.csv"
FALLBACK_FILE = "../nutrition_activity_obesity_usa_subset.csv"
# webserver.task_runner.start()

if os.path.exists(LOCAL_FILE):
    webserver.data_ingestor = DataIngestor(LOCAL_FILE)
else:
    webserver.data_ingestor = DataIngestor(FALLBACK_FILE)
```

## Resources Used

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Threading](https://docs.python.org/3/library/threading.html)
- [Pandas Docs](https://pandas.pydata.org/docs/)

## Git Repository
[https://github.com/denboba/web_server.git](https://github.com/denboba/web_server.git)
