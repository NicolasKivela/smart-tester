import json
import unittest
from ..app.test_script_generator.script_gen import ScriptGen
from io import StringIO
import sys

INPUT_PATH = "../test_test-scripts/"


class ScriptGenTests(unittest.TestCase):

    def test_correct_script(self):
        with open(INPUT_PATH + "correct_script_in.txt") as f:
            response = f.read()

        with open(INPUT_PATH + "correct_script_out.txt") as f:
            result = f.read()

        buffer = StringIO()
        sys.stdout = buffer

        obj = ScriptGen()
        obj.temp_collect_test_lines(response)
        obj.collect_keywords(response)
        obj.collect_variables(response)
        obj.scripts.append(response)

        assert result == json.loads(obj.assemble_result())["test_script"]
        assert buffer.getvalue() == ""

    def test_partially_correct_script(self):

        with open(INPUT_PATH + "partially_correct_script_in.txt") as f:
            response = f.read()

        with open(INPUT_PATH + "partially_correct_script_out.txt") as f:
            result = f.read()

        buffer = StringIO()
        sys.stdout = buffer

        obj = ScriptGen()
        obj.temp_collect_test_lines(response)
        obj.collect_keywords(response)
        obj.collect_variables(response)
        obj.scripts.append(response)

        expected_warnings = (
            "Successful keyword validation\n"
            "Successful keyword validation\n"
            "Warning: variable duplicate value mismatch: ${LOC_ROUTE}\n"
            "waring: '***' not found\n"
            "waring: unexpected text after: '***': <\n"
        )

        assert result == json.loads(obj.assemble_result())["test_script"]
        assert buffer.getvalue() == expected_warnings


    def test_combined_script(self):

        with open(INPUT_PATH + "correct_script_in.txt") as f:
            response_1 = f.read()

        with open(INPUT_PATH + "second_script_in.txt") as f:
            response_2 = f.read()

        with open(INPUT_PATH + "combined_script_out.txt") as f:
            result = f.read()

        buffer = StringIO()
        sys.stdout = buffer

        obj = ScriptGen()

        obj.temp_collect_test_lines(response_1)
        obj.collect_keywords(response_1)
        obj.collect_variables(response_1)
        obj.scripts.append(response_1)

        obj.temp_collect_test_lines(response_2)
        obj.collect_keywords(response_2)
        obj.collect_variables(response_2)
        obj.scripts.append(response_2)

        expected_warnings = "Warning: variable duplicate value mismatch: ${LOC_FROM_FIELD}\n"

        assert result == json.loads(obj.assemble_result())["test_script"]
        assert buffer.getvalue() == expected_warnings
