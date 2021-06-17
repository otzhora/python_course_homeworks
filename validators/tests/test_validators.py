import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from validators import validate_input, validate_output, validate_output_dict


@validate_input(
    'float',
    'int',
    'string'
)
def should_validate_input_base(a, b, c):
    pass


@validate_input(
    'number',
    'iterable'
)
def should_validate_input_syntetic(a, b):
    pass


@validate_output(
    'number'
)
def should_validate_output(val):
    return val


@validate_output_dict(
    key1='number',
    key2='iterable',
    key3='float'
)
def should_validate_output_dict(val):
    return val


class TestValidators(unittest.TestCase):
    def test_validate_input_base(self):
        should_validate_input_base(0.2, 3, 'str')

        with self.assertRaises(TypeError):
            should_validate_input_base(3, 3, 'str')

        with self.assertRaises(TypeError):
            should_validate_input_base(0.2, 0.2, 'str')

        with self.assertRaises(TypeError):
            should_validate_input_base(0.2, 3, 1)

        with self.assertRaises(AssertionError):
            @validate_input('int')
            def should_fail(a, b):
                pass

    def test_validate_input_syntetic(self):
        should_validate_input_syntetic(0.2, [])
        should_validate_input_syntetic(2, ())

        with self.assertRaises(TypeError):
            should_validate_input_syntetic([], [])

        with self.assertRaises(TypeError):
            should_validate_input_syntetic('str', [])

        with self.assertRaises(TypeError):
            should_validate_input_syntetic(2, 2)

    def test_validate_output(self):
        should_validate_output(1)
        should_validate_output(0.1)

        with self.assertRaises(TypeError):
            should_validate_output('str')

    def test_validate_output_dict(self):
        should_validate_output_dict({'key1': 1, 'key2': [], 'key3': 0.2})

        with self.assertRaises(TypeError):
            should_validate_output_dict({'key1': 'str', 'key2': [], 'key3': 0.2})

        with self.assertRaises(TypeError):
            should_validate_output_dict({'key1': 1, 'key2': 1, 'key3': 0.2})

        with self.assertRaises(TypeError):
            should_validate_output_dict({'key1': 1, 'key2': [], 'key3': 'str'})

        with self.assertRaises(KeyError):
            should_validate_output_dict({'key5': 1, 'key2': [], 'key3': 'str'})



if __name__ == "__main__":
    unittest.main()
