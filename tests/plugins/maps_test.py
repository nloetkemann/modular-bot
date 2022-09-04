import logging

from src.plugin_loader import PluginLoader
from src.plugins.maps import Maps
import os

from src.tools.method_thread import MethodThread


def test_map_image():
    image_name = Maps.get_map_by_name('Rahden')
    if os.path.isfile(image_name):
        os.remove(image_name)
        return True
    return False


def test_map_image_thread():
    photo_thread = MethodThread(Maps.get_map_by_name, 'Rahden')
    photo_thread.start()
    city_photo = photo_thread.join_get_response()
    if os.path.isfile(city_photo):
        os.remove(city_photo)
        return True
    return False


def test_city_info():
    loader = PluginLoader([{'name': 'maps'}])
    maps = loader.get_plugin('maps')
    result = maps.city_info({'$city': 'Rahden'})
    if os.path.isfile(result['__photo']):
        os.remove(result['__photo'])
        return True
    return False

