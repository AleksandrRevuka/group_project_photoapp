"""runner"""
import unittest

from tests import test_repository_comments, test_connect_db, test_repository_tags

ABTestSuite = unittest.TestSuite()
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_repository_comments.TestComments))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_connect_db.TestdConnectDB))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_repository_tags.TestTags))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(ABTestSuite)
