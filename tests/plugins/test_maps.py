from src.plugin_loader import PluginLoader
from src.plugins.maps import Maps
import os

from src.tools.method_thread import MethodThread

import unittest


class TestMaps(unittest.TestCase):

    def test_map_image(self):
        image_name = Maps.get_map_by_name('Rahden')
        self.assertEqual(os.path.isfile(image_name), True)
        if os.path.isfile(image_name):
            os.remove(image_name)

    def test_map_image_thread(self):
        photo_thread = MethodThread(Maps.get_map_by_name, 'Rahden')
        photo_thread.start()
        city_photo = photo_thread.join_get_response()
        self.assertEqual(os.path.isfile(city_photo), True)
        if os.path.isfile(city_photo):
            os.remove(city_photo)

    # def test_city_info(self):
    #     loader = PluginLoader([{'name': 'maps'}])
    #     maps = loader.get_plugin('maps')
    #     result = maps.city_info({'$city': 'Rahden'})
    #     self.assertEqual(os.path.isfile(result['__photo']), True)
    #     if os.path.isfile(result['__photo']):
    #         os.remove(result['__photo'])
