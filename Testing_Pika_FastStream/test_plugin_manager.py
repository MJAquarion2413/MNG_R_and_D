import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from plugin_manager import PluginManager


@pytest.fixture
async def plugin_manager():
    manager = PluginManager()
    await manager.setup_messaging()
    manager.load_plugins()
    return manager


@pytest.mark.asyncio
async def test_send_and_receive_message(plugin_manager):
    mock_plugin = MagicMock()
    plugin_manager.plugins = [mock_plugin]
    await plugin_manager.send_message("Hello, Plugin!")

    mock_plugin.handle_message.assert_called_with("Hello, Plugin!")
