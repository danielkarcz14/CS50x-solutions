from project import is_valid, get_option, get_contact_info
import unittest
from unittest.mock import patch


def test_is_valid():
    assert is_valid("+420 732 846 337") == True
    assert is_valid("+1 (123) 456-7890") == True
    assert is_valid("(555) 123-4567") == True
    assert is_valid("+44 20 7946 0958") == True
    assert is_valid("(123)-456-7890") == True
    assert is_valid("ABC-DEF-GHIJ") == False



class TestGetOption(unittest.TestCase):
    @patch('builtins.input', return_value='1')
    def test_get_option(self, input):
        self.assertEqual(get_option(), 1)

    @patch('builtins.input', return_value='2')
    def test_get_option(self, input):
        self.assertEqual(get_option(), 2)
    
    # First input is incorrect, followed by a correct input to prevent an infinite loop.
    # This will test if the user gets reprompted after the incorrect input, which is the expected behavior. 
    @patch('builtins.input', side_effect=['0', 1])
    def test_get_option_zero_then_one(self, input):
        self.assertEqual(get_option(), 1)

    # First input is incorrect, followed by a correct input to prevent an infinite loop.
    # This will test if the user gets reprompted after the incorrect input, which is the expected behavior. 
    @patch('builtins.input', side_effect=['string', 1])
    def test_get_option_string_then_one(self, input):
        self.assertEqual(get_option(), 1)


class TestGetContactInfo(unittest.TestCase):
    @patch('builtins.input', side_effect=['David', '123456789'])
    def test_get_contact_info(self, input):
        self.assertEqual(get_contact_info(), ('David', '123456789'))
