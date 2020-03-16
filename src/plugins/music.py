from src.yaml.plugin import Plugin
from PyLyrics import *


class Music(Plugin):
    def get_album(self, args):
        self.requiere_param(args, '$singer')
        singer_name = args['$singer']

        albums = PyLyrics.getAlbums(singer_name)

        result = ''
        for album in albums:
            result += '\n- {0} {1}'.format(album.name, album.year)

        return {'$result': result}

    def get_lyric(self, args):
        self.requiere_param(args, '$song')
        song_name = args['$song']

        if '$singer' in args:



        return {'$result': '', '$song': song_name}
