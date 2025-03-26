import requests
import json
import unittest

from datetime import datetime, timedelta
from time import sleep
import os

import sys
try:
    from io import StringIO
except:
    from StringIO import StringIO

import pylint.lint

from deepdiff import DeepDiff

total_score = 10
MAX_SCORE = 100

ONLY_LAST = False
PYLINT_LOCAL_DEBUG = True

START_TIMESTAMP = datetime.now()
GLOBAL_TIMEOUT_MINUTES = 5
GLOBAL_TIMEOUT_SECONDS = GLOBAL_TIMEOUT_MINUTES * 60

class TestAPI(unittest.TestCase):
    def check_global_timeout(self):
        current_timestamp = datetime.now()
        time_delta = current_timestamp - START_TIMESTAMP
        if time_delta.seconds > GLOBAL_TIMEOUT_SECONDS:
            self.fail("Checker absolute timeout. Checking took too long. Ending..")

    def check_res_timeout(self, res_callable, ref_result, timeout_sec, poll_interval = 0.2):
        initial_timestamp = datetime.now()
        while True:
            response = res_callable()
            # print(response)
        
            # Asserting that the response status code is 200 (OK)
            self.assertEqual(response.status_code, 200)
        
            # Asserting the response data
            response_data = response.json()
            # print(f"Response_data\n{response_data}")
            if response_data['status'] == 'done':
                # print(f"Response data {response_data['data']} and type {type(response_data['data'])}")
                # print(f"Ref data {ref_result} and type {type(ref_result)}")
                d = DeepDiff(response_data['data'], ref_result, math_epsilon=0.01)
                self.assertTrue(d == {}, str(d))
                break
            elif response_data['status'] == 'running':
                current_timestamp = datetime.now()
                time_delta = current_timestamp - initial_timestamp
                if time_delta.seconds > timeout_sec:
                    self.fail("Operation timedout")
                else:
                    sleep(poll_interval)
            else:
                self.fail(f"Job failed. Full response data:\n{json.dumps(response_data)}")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_states_mean(self):
        self.check_global_timeout()
        self.helper_test_endpoint("states_mean")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_state_mean(self):
        self.check_global_timeout()
        self.helper_test_endpoint("state_mean")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_best5(self):
        self.check_global_timeout()
        self.helper_test_endpoint("best5")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_worst5(self):
        self.check_global_timeout()
        self.helper_test_endpoint("worst5")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_global_mean(self):
        self.check_global_timeout()
        self.helper_test_endpoint("global_mean")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_diff_from_mean(self):
        self.check_global_timeout()
        self.helper_test_endpoint("diff_from_mean")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_state_diff_from_mean(self):
        self.check_global_timeout()
        self.helper_test_endpoint("state_diff_from_mean")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_mean_by_category(self):
        self.check_global_timeout()
        self.helper_test_endpoint("mean_by_category")

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_state_mean_by_category(self):
        self.check_global_timeout()
        self.helper_test_endpoint("state_mean_by_category")

    def helper_test_endpoint(self, endpoint):
        global total_score

        output_dir = f"tests/{endpoint}/output/"
        input_dir = f"tests/{endpoint}/input/"
        input_files = os.listdir(input_dir)

        test_suite_score = 10
        test_score = test_suite_score / len(input_files)
        local_score = 0

        for input_file in input_files:
            # Get the index from in-idx.json
            # The idx is between a dash (-) and a dot (.)
            idx = input_file.split('-')[1]
            idx = int(idx.split('.')[0])

            with open(f"{input_dir}/{input_file}", "r") as fin:
                # Data to be sent in the POST request
                req_data = json.load(fin)

            with open(f"{output_dir}/out-{idx}.json", "r") as fout:
                ref_result = json.load(fout)
            
            with self.subTest():
                # Sending a POST request to the Flask endpoint
                res = requests.post(f"http://127.0.0.1:5000/api/{endpoint}", json=req_data)

                job_id = res.json()
                # print(f'job-res is {job_id}')
                job_id = job_id["job_id"]

                self.check_res_timeout(
                    res_callable = lambda: requests.get(f"http://127.0.0.1:5000/api/get_results/{job_id}"),
                    ref_result = ref_result,
                    timeout_sec = 3)

                local_score += test_score
        total_score += min(round(local_score), test_suite_score)

    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_coding_style(self):
        global total_score
        self.check_global_timeout()

        python_files = []
        for root, _, files in os.walk("./app"):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        stdout = sys.stdout
        sys.stdout = StringIO()

        ARGS = ["-r", "n", "--rcfile=pylintrc"]
        r = pylint.lint.Run(python_files + ARGS, exit=False)

        test = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = stdout

        lint_res = test.split('\n')
        if PYLINT_LOCAL_DEBUG:
            print(f"\nPYLINT OUTPUT\n>>>>>>\n{test}<<<<<<\n")

        rating_str = "Your code has been rated at "
        score_line = list(filter(lambda ln: rating_str in ln, lint_res))[0]
        score_str = score_line.split(rating_str)[-1]
        score = float(score_str.split('/')[0])
        print(score_line)
        if score < 8:
            total_score -= 10
            self.fail("Low pylint score. Deducting 10 pts penalty.")

if __name__ == '__main__':
    try:
        os.system("rm -rf results/*")
        unittest.main()
    finally:
        print(f"Last checker run time is: {START_TIMESTAMP}")
        total_score = min(total_score, MAX_SCORE)
        print(f"Your final score is: {total_score}/{MAX_SCORE}")
        print(f"Total: {total_score}")
