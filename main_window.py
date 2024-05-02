# MainWindow.py
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QCheckBox, QListWidget, QDockWidget, QTextEdit, \
    QHBoxLayout, QApplication, QListWidgetItem, QPushButton
from PySide6.QtCore import Qt

from plugin_manager import PluginManager

import logging


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qt Plugin-based Application")
        self.setGeometry(100, 100, 800, 600)

        # loads plugins, and send access to GUI to plugin manager
        self.plugin_manager = PluginManager(self)
        self.plugin_widgets = {}

        self.initUI()

    def initUI(self):
        self.create_docking_area()
        self.create_plugin_control_panel()

    def create_docking_area(self):
        self.dock_widget_area = QWidget(self)
        self.setCentralWidget(self.dock_widget_area)
        self.dock_layout = QHBoxLayout(self.dock_widget_area)

    def create_plugin_control_panel(self):
        # Panel to enable/disable plugins
        self.plugin_control_panel = QListWidget(self)
        self.plugin_control_panel.setFixedWidth(200)

        plugin_names = ['plugin_A', 'plugin_B']
        for name in plugin_names:
            logging.info(f"Adding {name} to the plugin control panel")
            item = QListWidgetItem(self.plugin_control_panel)
            on_off_switch = QPushButton(f"Enable {name}", self.plugin_control_panel)
            on_off_switch.setCheckable(True)
            on_off_switch.setStyleSheet("""
                QPushButton {
                    background-color: red;  /* Default, 'off' state color */
                    color: white;  /* Text color */
                }
                QPushButton:checked {
                    background-color: green;  /* 'On' state color */
                    color: black;
                }
            """)
            on_off_switch.toggled.connect(lambda checked, name=name: self.enable_plugin(name) if checked else self.disable_plugin(name))
            item.setSizeHint(on_off_switch.sizeHint())
            self.plugin_control_panel.addItem(item)
            self.plugin_control_panel.setItemWidget(item, on_off_switch)


        # Add the plugin control panel as a dockable widget to the left
        control_dock = QDockWidget("Plugin Control", self)
        control_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)
        control_dock.setWidget(self.plugin_control_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, control_dock)

    def enable_plugin(self, plugin_name):
        print(f"Enable {plugin_name}")
        self.plugin_manager.load_plugin(plugin_name)
        self.add_plugin_to_dock(plugin_name)

    def disable_plugin(self, plugin_name):
        print(f"Disable {plugin_name}")
        self.plugin_manager.unload_plugin(plugin_name)
        self.remove_plugin_from_dock(plugin_name)

    def add_plugin_to_dock(self, plugin_name):
        color = 'green' if plugin_name == 'ButtonPlugin' else 'blue'
        plugin_widget = QTextEdit(f"Contents of {plugin_name}")  # Placeholder for actual plugin widget
        plugin_widget.setStyleSheet(f"background-color: {color};")
        dock = QDockWidget(plugin_name, self)
        dock.setWidget(plugin_widget)
        self.dock_layout.addWidget(dock)
        self.plugin_widgets[plugin_name] = dock

    def remove_plugin_from_dock(self, plugin_name):
        dock = self.plugin_widgets.get(plugin_name)
        if dock:
            self.dock_layout.removeWidget(dock)
            dock.close()
            del self.plugin_widgets[plugin_name]

    def closeEvent(self, event):
        # Clean up plugins before closing
        self.plugin_manager.unload_plugins()
        super().closeEvent(event)

    """
    def init_core_plugins(self):
        # Load core plugins
        self.plugin_manager.load_plugin('plugin_A')
        self.plugin_manager.load_plugin('plugin_B')
        self.add_plugin_to_dock('plugin_A')
        self.add_plugin_to_dock('plugin_B')
    """

