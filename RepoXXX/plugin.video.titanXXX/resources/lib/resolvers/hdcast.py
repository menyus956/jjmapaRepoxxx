# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re,urlparse
from resources.lib.libraries import client


def resolve(url):
    try:
        id = urlparse.parse_qs(urlparse.urlparse(url).query)['id'][0]

        pageUrl = 'http://hdcast.me/embedplayer.php?width=640&height=480&id=%s&autoplay=true&strech=exactfit' % id

        result = client.request(pageUrl, referer=url)

        x = re.compile('/file\s*: \s*[\'|\"](.+?)[\'|\"]').findall(result)

        url = re.compile('file\s*: \s*[\'|\"](.+?)[\'|\"]').findall(result)
        url = [i for i in url if not i in x]
        url = [i for i in url if 'rtmp' in i or  'm3u8' in i][0]

        if url.startswith('rtmp'): url += ' live=1 timeout=15'

        return url
    except:
        return

