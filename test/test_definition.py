from mock import mock, MagicMock
from mopidy_qobuz import Extension
from mopidy_qobuz.backend import QobuzBackend


def test_get_default_config():
    extension = Extension()

    config = extension.get_default_config()

    assert "[qobuz]" in config
    assert "enabled = true" in config
    assert "username =" in config
    assert "password =" in config
    assert "app_id =" in config
    assert "secrets =" in config


def test_get_config_schema():
    ext = Extension()
    schema = ext.get_config_schema()

    assert "enabled" in schema
    assert "username" in schema
    assert "password" in schema
    assert "app_id" in schema
    assert "secrets" in schema


def test_setup():
    registry = mock.Mock()

    ext = Extension()
    ext.setup(registry)
    calls = [mock.call("backend", QobuzBackend)]
    registry.add.assert_has_calls(calls, any_order=True)
