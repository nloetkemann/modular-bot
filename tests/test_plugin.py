import unittest

from tests.plugins.test_maps import TestMaps


def suite_plugin():
    suite = unittest.TestSuite()
    suite.addTest(TestMaps('test_map_image'))
    suite.addTest(TestMaps('test_map_image_thread'))
    return suite