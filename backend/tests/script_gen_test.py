import json
import unittest
from ..app.test_script_generator.script_gen import ScriptGen
from io import StringIO
import sys

INPUT_PATH = "tests/test_test-scripts/"
RESULT_KEY = "test_script"

class ScriptGenTests(unittest.TestCase):
    """
    Runs robotframework scripts through the text processing functions
    For more detail see the test_test-scripts folder see expected output and test input
    """
    maxDiff = None
    def test_correct_script(self):

        file = open(INPUT_PATH + "correct_script_in.txt")
        response = file.read()
        file.close()

        file = open(INPUT_PATH + "correct_script_out.txt")
        result = file.read()
        file.close()

        # capture std out to see if program prints warnings
        buffer = StringIO()
        sys.stdout = buffer
        file.close()

        obj = ScriptGen()
        obj.temp_collect_test_lines(response)
        obj.collect_keywords(response)
        obj.collect_variables(response)
        obj.scripts.append(response)

        self.assertEqual(result, json.loads(obj.assemble_result())[RESULT_KEY])
        self.assertEqual("", buffer.getvalue())

    def test_partially_correct_script(self):
        file = open(INPUT_PATH + "partially_correct_script_in.txt")
        response = file.read()
        file.close()

        file = open(INPUT_PATH + "partially_correct_script_out.txt")
        result = file.read()
        file.close()

        # capture std out to see if program prints warnings
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
            "Waring: Failed keyword: The this should fail\n"
            "Warning: variable duplicate value mismatch: ${LOC_ROUTE}\n"
            "Waring: '***' not found\n"
            "Waring: unexpected text after: '***': <\n"
            "Warning: 1 failed keywords\n"
        )

        self.assertEqual(result, json.loads(obj.assemble_result())[RESULT_KEY])
        self.assertEqual(expected_warnings, buffer.getvalue())


    def test_combined_script(self):

        file = open(INPUT_PATH + "correct_script_in.txt")
        response_1 = file.read()
        file.close()

        file = open(INPUT_PATH + "second_script_in.txt")
        response_2 = file.read()
        file.close()

        file = open(INPUT_PATH + "combined_script_out.txt")
        result = file.read()
        file.close()

        # capture std out to see if program prints warnings
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

        self.assertEqual(result, json.loads(obj.assemble_result())[RESULT_KEY])
        self.assertEqual(expected_warnings, buffer.getvalue())

    def test_invalid_script(self):

        file = open(INPUT_PATH + "invalid_in.txt")
        response = file.read()
        file.close()

        file = open(INPUT_PATH + "invalid_out.txt")
        result = file.read()
        file.close()

        # capture std out to see if program prints warnings
        buffer = StringIO()
        sys.stdout = buffer

        obj = ScriptGen()
        obj.temp_collect_test_lines(response)
        obj.collect_keywords(response)
        obj.collect_variables(response)
        obj.scripts.append(response)

        expected_warnings = (
            "Warning: No test cases found.\n"
            "Warning: No keywords found.\n"
            "Warning: No variables found.\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: '***' not found\n"
            "Waring: unexpected text after: '***': J\n"
        )

        self.assertEqual(result, json.loads(obj.assemble_result())[RESULT_KEY])
        self.assertEqual(expected_warnings, buffer.getvalue())

