"""runner"""
import unittest

from tests import (test_connect_db, test_repository_comments,
                   test_repository_pictures, test_repository_tags,
                   test_route_comment, test_route_tags)

ABTestSuite = unittest.TestSuite()
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_route_comment.TestRoutComment))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_repository_comments.TestRepositoryComments))

ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_connect_db.TestdConnectDB))

ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_repository_tags.TestRepositoryTags))
ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_route_tags.TestRouteTags))

ABTestSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_repository_pictures.TestRepositoryPictures))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(ABTestSuite)
