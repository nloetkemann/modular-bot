from src.config import Config
from src.plugin_loader import PluginLoader

plugins = []

if __name__ == '__main__':
    config = Config()
    loader = PluginLoader(config.plugins)
