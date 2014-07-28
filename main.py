import json
import traceback

from couchpotato.core.helpers.variable import tryInt
from couchpotato.core.logger import CPLog
from couchpotato.core.media._base.providers.torrent.base import TorrentProvider
from couchpotato.core.media.movie.providers.base import MovieProvider

log = CPLog(__name__)

# Norbits API details:
# Quality param:
# 720p=20, 1080p=19, SD=22

# Medium param:
# DVD=26, Blu-ray=27, Encode=29

# Codec param:
# x264=9,xvid=10


class Norbits(TorrentProvider, MovieProvider):

    urls = {
        'test': 'https://norbits.net/',
        'detail': 'https://norbits.net/details.php?id=%s',
        'download': 'https://norbits.net/download.php?id=%s&passkey=%s',
        'api': 'https://norbits.net/api2.php?action=torrents'
    }
    http_time_between_calls = 1  # Seconds

    def getNorbitsQuality(self, quality):
        # Return the proper quality ID to use in the API, defaults to None which searchs for everything
        return {
            '1080p': 19,
            'brrip': 19,
            '720p': 20,
            'dvdrip': 22,
            'dvd': 22
        }.get(quality, None)

    def _post_query(self, search, quality=None):

        post_data = {
            'username': self.conf('username'),
            'passkey': self.conf('passkey'),
            'category': '1',
            'search': search
        }

        if quality:
            post_data.update({'quality': quality})

        try:
            result = self.getJsonData(self.urls['api'], data=json.dumps(post_data))
            if result:
                if int(result['status']) != 0:
                    log.error('Error searching norbits: %s' % result['message'])
                else:
                    return result['data']['torrents']
        except:
            pass
        return None

    def _searchOnTitle(self, title, media, quality, results):
        data = self._post_query(title, self.getNorbitsQuality(quality.get('custom').get('quality')))
        if data:
            try:
                for result in data:
                    results.append({
                        'id': result['id'],
                        'name': result['name'],
                        'url': self.urls['download'] % (result['id'], self.conf('passkey')),
                        'detail_url': self.urls['detail'] % result['id'],
                        'size': tryInt(int(result['size']) / 1024 / 1024)
                        #'seeders': 1, # FIXME: this is currently missing in the API response
                        #'leechers': 1, # FIXME: this is currently missing in the API response
                    })
            except:
                log.error('Failed getting resutls from %s: %s' % (self.getName(), traceback.format_exc()))
