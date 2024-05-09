import pytest
from faststream import FastStream
from plugin_manager import PluginManager


@pytest.fixture
def fast_stream():
    return FastStream()


def test_plugin_lifecycle(fast_stream):
    manager = PluginManager(fast_stream)
    manager.load_plugins()

    # Simulate lifecycle
    fast_stream.run_in_thread(startup=True)
    fast_stream.run_in_thread(shutdown=True)

    # Assertions would be based on expected outcomes, such as logs or state changes in plugins
