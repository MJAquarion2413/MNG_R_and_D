import sys
from PySide6.QtWidgets import QApplication
from plugin_manager import PluginManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = PluginManager()
    manager.load_plugins()
    manager.initialize()
    sys.exit(app.exec_())
