import logging
import unittest

from tests.test_plugin import suite_plugin
from tests.test_plugin_handler import TestPluginHandler

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
threads = {}

test_suite = unittest.TestSuite()
test_suite.addTest(TestPluginHandler('test_validate_user_input'))
test_suite.addTest(suite_plugin())
runner = unittest.TextTestRunner()
runner.run(test_suite)
