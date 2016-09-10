#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import traceback

from couchpotato.core.helpers.variable import tryInt, getIdentifier
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
        'download': 'https://norbits.net/download.php',
        'download2': 'https://norbits.net/download.php?id=%s&passkey=%s',
        'api': 'https://norbits.net/api2.php?action=torrents'
    }
    http_time_between_calls = 1  # Seconds

    def getDownloadUrl(self, download_id):
        pkey = self.conf('passkey')
        download_url = self.urls['download'] + '?passkey=%s&id=%s' % (pkey, download_id)
        log.info('Created download_url: %s' % download_url)
        return download_url

    def getNorbitsQuality(self, quality):
        # Return the proper quality ID to use in the API, defaults to None which searchs for everything
        return {
            '1080p': 19,
            'brrip': 22,
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
            log.debug('Searching with data: %s' % json.dumps(post_data))
            result = self.getJsonData(self.urls['api'], data=json.dumps(post_data))
            log.debug('Result: %s' % result)
            if result:
                log.debug('We got: %s ' % json.dumps(result))
                if int(result['status']) != 0:
                    log.error('Error searching norbits because of wrong status: %s' % result['message'])
                    log.error('Result: %s' % result)
                else:
                    result_data = result['data']
                    if int(result_data['total']) < 1:
                        log.info('Nothing found for %s' % search)
                        return None
                    else:
                        return result_data['torrents']
        except Exception, e:
            log.error('Error searching norbits due to exception: %s. type: %s Result: %s' % (e, type(e), result))
        return None

    def _search(self, movie, quality, results):
        title = getIdentifier(movie)
        data = self._post_query(title, self.getNorbitsQuality(quality.get('custom').get('quality')))
        if data:
            log.info('We got data: %s' % data)
            try:
                for result in data:
                    log.info('We got result: %s' % result)
                    download_url = self.getDownloadUrl(result['id'])
                    details_url = self.urls['detail'] % result['id']
                    log.info('Download url: %s' % download_url)
                    log.info('Details url: %s' % details_url)
                    append_data = {
                        'id': result['id'],
                        'name': result['name'],
                        'detail_url': details_url,
                        'size': tryInt(int(result['size']) / 1024 / 1024),
                        'seeders': tryInt(result['seeders']),
                        'leechers': tryInt(result['leechers']),
                        'url': download_url
                    }
                    log.info('Appending data: %s' % json.dumps(append_data))
                    results.append(append_data)
            except:
                log.error('Failed getting resutls from %s: %s' % (self.getName(), traceback.format_exc()))
            finally:
                log.info('Final results: %s' % results)
        return results
