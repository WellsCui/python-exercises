import unittest
import org.wells.examples as examples
from unittest.mock import patch


class ExampleTest(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    @patch('org.wells.examples.Employee')
    def test_employee(self, mockClass1):
        print("mocking employee...")
        examples.Employee("well", 100)
        print(examples.Employee.displayEmployeeCount())
        assert mockClass1 is examples.Employee
        assert mockClass1.called

if __name__ == '__main__':
    unittest.main()