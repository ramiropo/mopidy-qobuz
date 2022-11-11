from __future__ import unicode_literals

import logging

from mopidy import audio, backend

logger = logging.getLogger(__name__)


class QobuzPlaybackProvider(backend.PlaybackProvider):
    def __init__(self, audio, backend):
        super(QobuzPlaybackProvider, self).__init__(audio, backend)

        self.delta = 0

    def translate_uri(self, uri):
        """Get file-URL for a track-uri in mopidy.

        Parameters
        ----------
        uri: str
            Mopidy URI of a track
        """
        parts = uri.split(":")
        track_id = int(parts[4])

        newurl = self.backend.client.api_call("track/getFileUrl", id=track_id, fmt_id=5)
        logger.debug(f"Playback URL: {newurl}")

        return newurl["url"]

    def seek(self, time_position):
        return super(QobuzPlaybackProvider, self).seek(time_position)

    def stop(self):
        return super(QobuzPlaybackProvider, self).stop()

    def play(self):
        return super(QobuzPlaybackProvider, self).play()
