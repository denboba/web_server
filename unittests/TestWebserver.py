import json
import unittest
import os
from data_ingestor import DataIngestor

data_ingestor = DataIngestor("../nutrition_activity_obesity_usa_subset.csv")


class TestWebserver(unittest.TestCase):

    def test_read_file(self):
        self.assertIsNotNone(data_ingestor.df)

    def test_states_mean(self):
        # read input and output files from the tests/states_mean/input and tests/states_mean/output directories
        # for each input file, call the states_mean function and compare the output with the corresponding output file
        for i in range(1, len(os.listdir("../tests/states_mean/input")) + 1):
            with open(f"../tests/states_mean/input/in-{i}.json", 'r') as f:
                question = f.read().strip()
            with open(f"../tests/states_mean/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.states_mean(question)
        if result != expected_output:
            print(f"Test failed for question{i}: {question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_state_mean(self):
        for i in range(1, len(os.listdir("../tests/state_mean/input")) + 1):
            with open(f"../tests/state_mean/input/in-{i}.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(f"../tests/state_mean/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.state_mean(data['question'], data['state'])
        if result != expected_output:
            print(f"Test failed for question: {i}: {data['question']}, state: {data['state']}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_best5(self):
        for i in range(1, len(os.listdir("../tests/best5/input")) + 1):
            with open(f"../tests/best5/input/in-{i}.json", 'r') as f:
                question = f.read().strip()
            with open(f"../tests/best5/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.best5(question)
        if result != expected_output:
            print(f"Test failed for question: {i}: {question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")

        self.assertEqual(result, expected_output)

    def test_worst5(self):
        for i in range(1, len(os.listdir("../tests/worst5/input")) + 1):
            with open(f"../tests/worst5/input/in-{i}.json", 'r') as f:
                question = f.read().strip()
            with open(f"../tests/worst5/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.worst5(question)
        if result != expected_output:
            print(f"Test failed for question: {i}: {question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_global_mean(self):
        for i in range(1, len(os.listdir("../tests/global_mean/input")) + 1):
            with open(f"../tests/global_mean/input/in-{i}.json", 'r') as f:
                question = f.read().strip()
            with open(f"../tests/global_mean/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.global_mean(question)
        if result != expected_output:
            print(f"Test failed for question: {i}: {question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_diff_from_mean(self):
        for i in range(1, len(os.listdir("../tests/diff_from_mean/input")) + 1):
            with open(f"../tests/diff_from_mean/input/in-{i}.json", 'r') as f:
                question = f.read().strip()
            with open(f"../tests/diff_from_mean/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.diff_from_mean(question)
        if result != expected_output:
            print(f"Test failed for question: {i}: {question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_state_diff_from_mean(self):
        for i in range(1, len(os.listdir("../tests/state_diff_from_mean/input")) + 1):
            with open(f"../tests/state_diff_from_mean/input/in-{i}.json", 'r') as f:
                data = json.load(f)
            with open(f"../tests/state_diff_from_mean/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.state_diff_from_mean(data['question'], data['state'])
        if result != expected_output:
            print(f"Test failed for question: {i}: {data['question']}, state: {data['state']}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_mean_by_category(self):
        for i in range(1, len(os.listdir("../tests/mean_by_category/input")) + 1):
            with open(f"../tests/mean_by_category/input/in-{i}.json", 'r') as f:
                question = f.read().strip()
            with open(f"../tests/mean_by_category/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.mean_by_category(question)
        if result != expected_output:
            print(f"Test failed for question: {i}: {question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)

    def test_state_mean_by_category(self):
        for i in range(1, len(os.listdir("../tests/state_mean_by_category/input")) + 1):
            with open(f"../tests/state_mean_by_category/input/in-{i}.json", 'r') as f:
                data = json.load(f)
            with open(f"../tests/state_mean_by_category/output/out-{i}.json", 'r') as f:
                expected_output = f.read().strip()
        result = data_ingestor.state_mean_by_category(data['question'], data['state'])
        if result != expected_output:
            print(f"Test failed for question: {i}: {data['question']}, state: {data['state']}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {result}")
        self.assertEqual(result, expected_output)
