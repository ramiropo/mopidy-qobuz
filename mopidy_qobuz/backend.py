import logging
import pykka
from mopidy import backend
from mopidy_qobuz import library, playback  # , playlists
from qobuz_dl.qopy import Client


logger = logging.getLogger(__name__)


class QobuzBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(QobuzBackend, self).__init__()

        self._config = config
        self._session = None

        self.library = library.QobuzLibraryProvider(backend=self)
        self.playback = playback.QobuzPlaybackProvider(audio=audio, backend=self)
        # self.playlists = playlists.QobuzPlaylistsProvider(backend=self)
        self.uri_schemes = ["qobuz"]

    def on_start(self):

        self.client = Client(
            self._config["qobuz"]["username"],
            self._config["qobuz"]["password"],
            self._config["qobuz"]["app_id"],
            self._config["qobuz"]["secrets"].split(","),
        )
