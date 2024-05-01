import importlib
import logging

import os
from pathlib import Path
from signal_warehouse import SignalWarehouse


class PluginManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.signal_warehouse = SignalWarehouse()
        self.plugins = {}  # Dictionary to store loaded plugins
        self.load_plugins()

    def load_plugins(self):
        plugins_path = Path(__file__).parent / "plugins"  # Determine the plugin directory path

        print(f"Loading plugins from {plugins_path}")

        plugin_files = [f.stem for f in plugins_path.glob("*.py") if
                        f.name != "__init__.py"]  # List all .py files except __init__.py

        for plugin_name in plugin_files:
            module = importlib.import_module(f'plugins.{plugin_name}')  # Dynamically import the plugin module
            plugin = module.Plugin(self.main_window, self.signal_warehouse)  # Instantiate the plugin
            self.plugins[plugin_name] = plugin  # Store the plugin instance
            plugin.enable()  # Enable the plugin

    def unload_plugins(self):
        for plugin in self.plugins.values():
            plugin.disable()
        self.plugins.clear()

    def reload_plugins(self):
        self.unload_plugins()
        self.load_plugins()

    def load_plugin(self, plugin_name):
        if plugin_name not in self.plugins:
            module = importlib.import_module(f'plugins.{plugin_name}')
            plugin = module.Plugin(self.main_window, self.signal_warehouse)
            self.plugins[plugin_name] = plugin
            plugin.enable()

    def unload_plugin(self, plugin_name):
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.disable()
            del self.plugins[plugin_name]
