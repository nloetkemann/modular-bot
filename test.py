import logging

from tests.test_suits import test_plugins

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
threads = {}


def run_tests():
    test_plugins()


run_tests()
