import pytest
from example_plugin import ExamplePlugin
from unittest.mock import MagicMock

@pytest.fixture
def test_handle_message():
    plugin = ExamplePlugin()
    plugin.handle_stream_data = MagicMock(name='handle_stream_data')
    plugin.handle_message("Test Data")

    plugin.handle_stream_data.assert_called_with("Test Data")
