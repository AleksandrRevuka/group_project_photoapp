"""runner"""
import unittest

from tests import test_repository_comments, test_connect_db

ABTestSuite = unittest.TestSuite()
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_repository_comments.TestNotes))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_connect_db.TestdConnectDB))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(ABTestSuite)
