import logging

from tests.plugins.maps_test import test_map_image, test_map_image_thread, test_city_info


def test_plugins():
    logging.info(f'Map Image Tests Status: {test_map_image()}')
    logging.info(f'Map Image Thread Tests Status: {test_map_image_thread()}')
    logging.info(f'Map Image City Info Tests Status: {test_city_info()}')
