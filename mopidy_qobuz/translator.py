import logging
from mopidy import models

logger = logging.getLogger(__name__)


def to_artist(qobuz_artist):
    if qobuz_artist is None:
        return

    return models.Artist(
        uri="qobuz:artist:" + str(qobuz_artist["id"]),
        name=qobuz_artist["name"],
        sortname=qobuz_artist["slug"],
    )


def to_artist_ref(qobuz_artist):
    if qobuz_artist is None:
        return

    return models.Ref.artist(
        uri="qobuz:artist:" + str(qobuz_artist["id"]), name=qobuz_artist["name"]
    )


def to_album(qobuz_album, qobuz_artist=None):
    if qobuz_album is None:
        return

    return models.Album(
        uri="qobuz:album:" + str(qobuz_album["id"]),
        name=qobuz_album["title"] + (" (HD)" if is_hd(qobuz_album) else ""),
        artists=[
            to_artist(qobuz_album["artist"])
            if not qobuz_artist
            else to_artist(qobuz_artist)
        ],
        num_discs=qobuz_album["media_count"],
        num_tracks=qobuz_album["tracks_count"],
        date=qobuz_album["release_date_original"],
    )


def to_album_ref(qobuz_album):
    if qobuz_album is None:
        return

    return models.Ref.album(
        uri="qobuz:album:" + str(qobuz_album["id"]),
        name="{} - {}".format(qobuz_album["artist"]["name"], qobuz_album["title"]),
    )


def to_track(qobuz_track, qobuz_album=None, qobuz_artist=None):
    if qobuz_track is None:
        return

    album = None
    album_id = None
    artist = None
    artist_id = None
    if "album" in qobuz_track and qobuz_track["album"]:
        album = to_album(qobuz_track["album"])
        album_id = qobuz_track["album"]["id"]

        if "artist" in qobuz_track["album"] and qobuz_track["album"]["artist"]:
            artist = to_artist(qobuz_track["album"]["artist"])
            artist_id = qobuz_track["album"]["artist"]["id"]

    else:
        if qobuz_album:
            album = to_album(qobuz_album, qobuz_artist)
            album_id = qobuz_album["id"]
        if qobuz_artist:
            artist = to_artist(qobuz_artist)
            artist_id = qobuz_artist["id"]

    return models.Track(
        uri="qobuz:track:{0}:{1}:{2}".format(
            artist_id,
            album_id,
            qobuz_track["id"],
        ),
        name=qobuz_track["title"] + (" (HD)" if is_hd(qobuz_track) else ""),
        artists=[artist],
        album=album,
        length=qobuz_track["duration"] * 1000,  # s -> ms
        disc_no=qobuz_track["media_number"],
        track_no=qobuz_track["track_number"],
        bitrate=int(
            float(qobuz_track["maximum_sampling_rate"])
            * 1000
            * int(qobuz_track["maximum_bit_depth"])
            * int(qobuz_track["maximum_channel_count"])
        ),
        date=album.date,
    )


def to_track_ref(qobuz_track):
    if qobuz_track is None:
        return

    return models.Ref.track(
        uri="qobuz:track:{0}:{1}:{2}".format(
            qobuz_track.artists[0].id,
            qobuz_track.album.id,
            qobuz_track.id,
        ),
        name=qobuz_track.title,
    )


def to_playlist(qobuz_playlist):
    if qobuz_playlist is None:
        return

    return models.Playlist(
        uri="qobuz:playlist:{}".format(qobuz_playlist.id),
        name=qobuz_playlist.name,
        tracks=qobuz_playlist.get_tracks(limit=500),
    )


def to_playlist_ref(qobuz_playlist):
    if qobuz_playlist is None:
        return

    return models.Ref.playlist(
        uri="qobuz:playlist:{}".format(qobuz_playlist.id),
        name=qobuz_playlist.name,
    )


def is_hd(qobuz_item) -> bool:
    return (
        qobuz_item["maximum_sampling_rate"] > 44.1
        or qobuz_item["maximum_bit_depth"] > 16
    )
