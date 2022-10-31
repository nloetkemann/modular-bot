import logging
import unittest

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d.%m.%Y %H:%M:%S ',
                    handlers=[logging.StreamHandler(), logging.FileHandler('./logs/tests.txt', mode='w')])


def load_tests(list_names, path_format: str) -> [unittest.TestCase]:
    tests_classes = []
    for name in list_names:
        include_path = path_format.format(name)
        test_name = f'Test{name[0].upper()}{name[1:]}'
        test_class = getattr(__import__(include_path, fromlist=[test_name]), test_name)
        tests_classes.append(test_class)
    return tests_classes


def run_plugin_tests(list_plugins):
    tests = load_tests(list_plugins, 'plugins.{0}.tests.{0}')
    suite = unittest.TestSuite()
    for plugin_test in tests:
        plugin_suite = unittest.TestSuite()
        plugin_tests = plugin_test.tests()
        plugin_suite.addTests(list(plugin_tests))
        suite.addTest(plugin_suite)
    runner = unittest.TextTestRunner()
    logging.info(f'Test Count: {suite.countTestCases()}')
    runner.run(suite)


def run():
    run_plugin_tests(['maps', 'checklist'])


run()
