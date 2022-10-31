from plugins.maps.maps import Maps
import os

from src.plugin_test import PluginTest
from src.tools.method_thread import MethodThread


class TestMaps(PluginTest):

    @staticmethod
    def get_test_obj_name():
        return 'maps'

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

    @staticmethod
    def tests():
        return TestMaps('test_map_image'), TestMaps('test_map_image_thread')
