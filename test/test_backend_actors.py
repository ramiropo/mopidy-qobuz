import pytest
from mock import mock
import mopidy_qobuz


@pytest.fixture
def config():
    return {
        "http": {"hostname": "127.0.0.1", "port": "6680"},
        "proxy": {"hostname": "host_mock", "port": "port_mock"},
        "qobuz": {
            "enabled": True,
            "username": "user@mail.com",
            "password": "SuperPass123!",
            "app_id": "2132344",
            "secrets": ",S1,S2",
        },
    }


def get_backend(config):
    return mopidy_qobuz.backend.QobuzBackend(config=config, audio=mock.Mock())


def test_uri_schemes(config):
    backend = get_backend(config)

    assert "qobuz" in backend.uri_schemes


def test_init_sets_up_the_providers(config):
    backend = get_backend(config)

    assert isinstance(backend.library, mopidy_qobuz.library.QobuzLibraryProvider)
    assert isinstance(backend.playback, mopidy_qobuz.playback.QobuzPlaybackProvider)
