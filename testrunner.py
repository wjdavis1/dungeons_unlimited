import unittest
from tests.users import user_tests

# Unit Test Runner - For all unit tests in the application


loader = unittest.TestLoader()
suite = unittest.TestSuite()

# suite.addTests(loader.loadTestsFromModule(INSERT_MODULE_HERE))
suite.addTests(loader.loadTestsFromModule(user_tests))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
