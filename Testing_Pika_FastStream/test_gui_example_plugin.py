import pytest
from pytestqt.qtbot import QtBot
from example_plugin import ExamplePlugin
from faststream import FastStream


@pytest.fixture
def fast_stream():
    return FastStream()


@pytest.fixture
def test_plugin_lifecycle(qtbot: QtBot, fast_stream: FastStream, capsys):
    plugin = ExamplePlugin(fast_stream)
    qtbot.addWidget(plugin)

    # Simulate startup and shutdown
    with qtbot.waitSignal(plugin.data_ready, timeout=1000):
        fast_stream.run()

    assert "Plugin setup tasks..." in capsys.readouterr().out
    assert "Plugin cleanup tasks..." in capsys.readouterr().out
