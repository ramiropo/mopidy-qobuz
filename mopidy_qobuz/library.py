from __future__ import unicode_literals

import logging
import qobuz
from collections import namedtuple
from mopidy import backend, models
from mopidy.models import Image, SearchResult
from mopidy_qobuz import translator
from mopidy_qobuz import browse

try:
    from functools import lru_cache
except ImportError:
    # python2
    from backports.functools_lru_cache import lru_cache


logger = logging.getLogger(__name__)


class QobuzLibraryProvider(backend.LibraryProvider):
    root_directory = models.Ref.directory(uri="qobuz:directory", name="Qobuz")

    def __init__(self, *args, **kwargs):
        super(QobuzLibraryProvider, self).__init__(*args, **kwargs)

    def browse(self, uri):
        if uri.startswith(self.root_directory.uri):
            return browse.browse_directory(uri, self.backend._session)
        else:
            return browse.browse_details(uri, self.backend._session)

    def search(self, query=None, uris=None, exact=False):
        field = list(query.keys())[0]
        value = list(query.values())[0]

        if len(value[0]) <= 3:
            logger.info(f"Query too short: {value}")
            return None

        if field == "artist":
            results = self.backend.client.search_artists(value, 10)
            logger.debug(results)
            artists = list(map(translator.to_artist, results["artists"]["items"]))
            return SearchResult(artists=artists)
        elif field == "album":
            results = self.backend.client.search_albums(value, 10)
            logger.debug(results)
            albums = list(map(translator.to_album, results["albums"]["items"]))
            return SearchResult(albums=albums)
        elif field == "track_name":
            results = self.backend.client.search_tracks(value, 10)
            logger.debug(results)
            tracks = list(map(translator.to_track, results["tracks"]["items"]))
            return SearchResult(tracks=tracks)

        artists = [translator.to_artist(a) for a in qobuz.Artist.search(value)]
        albums = [translator.to_album(a) for a in qobuz.Album.search(value)]
        tracks = [translator.to_track(t) for t in qobuz.Track.search(value)]
        return SearchResult(artists=artists, albums=albums, tracks=tracks)

    @lru_cache(maxsize=2048)
    def lookup(self, uri):
        parts = uri.split(":")

        if uri.startswith("qobuz:artist"):
            # qobuz:artist:artist_id
            artist_generator = self.backend.client.get_artist_meta(id=parts[2])

            tracks = []
            for artist in artist_generator:
                for album in artist["albums"]["items"]:
                    full_album = self.backend.client.get_album_meta(album["id"])

                    tracks += [
                        translator.to_track(track, full_album, full_album["artist"])
                        for track in full_album["tracks"]["items"]
                    ]

            return tracks

        elif uri.startswith("qobuz:track:"):
            return [
                translator.to_track(
                    self.backend.client.api_call("track/get", id=parts[4])
                )
            ]

        elif uri.startswith("qobuz:album"):
            # qobuz:album:album:id
            album = self.backend.client.api_call("album/get", id=parts[2])
            rta = [
                translator.to_track(track, album, album["artist"])
                for track in album["tracks"]["items"]
            ]

            return rta

        logger.warning('Failed to lookup "%s"', uri)
