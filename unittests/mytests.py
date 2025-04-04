import json
import unittest
import os
from app.data_ingestor import DataIngestor

data_ingestor = DataIngestor("../nutrition_activity_obesity_usa_subset.csv")


class TestWebserver(unittest.TestCase):

    def test_read_file(self):
        self.assertIsNotNone(data_ingestor.df)

    def test_states_mean(self):
        for i in range(1, len(os.listdir("../tests/states_mean/input"))):
            with open(f"../tests/states_mean/input/in-{i}.json", 'r') as f:
                question = json.load(f)['question']
            with open(f"../tests/states_mean/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.states_mean(question)
            self.assertEqual(result, expected_output)

    def test_state_mean(self):
        for i in range(1, len(os.listdir("../tests/state_mean/input")) + 1):
            with open(f"../tests/state_mean/input/in-{i}.json", 'r') as f:
                data = json.load(f)
            with open(f"../tests/state_mean/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.state_mean(data['question'], data['state'])
            self.assertEqual(result.keys(), expected_output.keys())
            for state in result:
                self.assertAlmostEqual(result[state], expected_output[state], places=6)


    def test_best5(self):
        for i in range(1, len(os.listdir("../tests/best5/input")) + 1):
            with open(f"../tests/best5/input/in-{i}.json", 'r') as f:
                question = json.load(f)['question']
            with open(f"../tests/best5/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.best5(question)
            self.assertEqual(result, expected_output)

    def test_worst5(self):
        for i in range(1, len(os.listdir("../tests/worst5/input")) + 1):
            with open(f"../tests/worst5/input/in-{i}.json", 'r') as f:
                question = json.load(f)['question']
            with open(f"../tests/worst5/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.worst5(question)
            self.assertEqual(result, expected_output)

    def test_global_mean(self):
        for i in range(1, len(os.listdir("../tests/global_mean/input")) + 1):
            with open(f"../tests/global_mean/input/in-{i}.json", 'r') as f:
                question = json.load(f)['question']
            with open(f"../tests/global_mean/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.global_mean(question)
            self.assertEqual(result, expected_output)

    def test_diff_from_mean(self):
        for i in range(1, len(os.listdir("../tests/diff_from_mean/input")) + 1):
            with open(f"../tests/diff_from_mean/input/in-{i}.json", 'r') as f:
                question = json.load(f)['question']
            with open(f"../tests/diff_from_mean/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.diff_from_mean(question)
            self.assertEqual(result, expected_output)

    def test_state_diff_from_mean(self):
        for i in range(1, len(os.listdir("../tests/state_diff_from_mean/input")) + 1):
            with open(f"../tests/state_diff_from_mean/input/in-{i}.json", 'r') as f:
                data = json.load(f)
            with open(f"../tests/state_diff_from_mean/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.state_diff_from_mean(data['question'], data['state'])
            self.assertEqual(result.keys(), expected_output.keys())
            for state in result:
                self.assertAlmostEqual(result[state], expected_output[state], places=6)

    def test_mean_by_category(self):
        for i in range(1, len(os.listdir("../tests/mean_by_category/input")) + 1):
            with open(f"../tests/mean_by_category/input/in-{i}.json", 'r') as f:
                question = json.load(f)['question']
            with open(f"../tests/mean_by_category/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.mean_by_category(question)
            self.assertEqual(result, expected_output)

    def test_state_mean_by_category(self):
        for i in range(1, len(os.listdir("../tests/state_mean_by_category/input")) + 1):
            with open(f"../tests/state_mean_by_category/input/in-{i}.json", 'r') as f:
                data = json.load(f)
            with open(f"../tests/state_mean_by_category/output/out-{i}.json", 'r') as f:
                expected_output = json.load(f)
            result = data_ingestor.state_mean_by_category(data['question'], data['state'])
            self.assertEqual(result.keys(), expected_output.keys())
            for state in result:
                self.assertAlmostEqual(result[state], expected_output[state], places=6)
