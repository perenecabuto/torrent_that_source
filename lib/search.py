# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
from model import Torrent, Movie, Audio
from model import TorrentSearch, MovieSearch
import re


def get_url_nodes(url):
    # if url == "http://www.hot100brasil.com/chtsinglesb.html":
    #     try:
    #         f = file('fixture.html', 'r')
    #         return BeautifulSoup(f.read())
    #     except Exception, e:
    #         raise e
    #     finally:
    #         f.close()
    # else:
        return BeautifulSoup(urlopen(url).read())


def for_musics(torrent_search_class, source):
    musics = Hot100BrasilSearch(source).items()

    for music in musics:
        music.torrents = torrent_search_class(
            music.search_terms(),
            source['type']
        ).torrents()
    return musics


def for_movies(torrent_search_class, source):
    movies = ImbdSearch(source).items()

    for movie in movies:
        movie.torrents = torrent_search_class(
            movie.search_terms(),
            source['type']
        ).torrents()
    return movies


class ImbdSearch(MovieSearch):

    def __init__(self, source):
        self.url = source['url']
        self.items_selector = source['items_selector']
        self.name_item = source['name_item']
        self.genre_item = source['genre_item']
        self.image_item = source['image_item']
        self.synopsis_item = source['synopsis_item']

    def items(self):
        items = []
        doc = get_url_nodes(self.url)
        list = doc.select(self.items_selector)

        for item in list:
            try:
                items.append(Movie(
                    title=item.select(self.name_item)[0].text,
                    image=item.select(self.image_item)[0].get('src'),
                    synopsis=item.select(self.synopsis_item)[0].text,
                    genre=", ".join([g.text for g in item.select(self.genre_item) or []]),
                ))
            except:
                next

        return items


class Hot100BrasilSearch(MovieSearch):

    def __init__(self, source):
        self.url = source['url']
        self.items_selector = source['items_selector']
        self.name_item = source['name_item']
        self.artist_item = source['artist_item']
        self.label_item = source['label_item']

    def items(self):
        items = []
        doc = get_url_nodes(self.url)
        list = doc.select(self.items_selector)

        for item in list:
            try:
                items.append(Audio(
                    title=item.select(self.name_item)[4].text.strip(),
                    artist=item.select(self.artist_item)[5].text.strip(),
                    label=item.select(self.label_item)[6].text.strip()
                ))
            except:
                next

        return items


class PirateBaySearch(TorrentSearch):
    SEARCH_TYPES = {
        'video': 200,
        'audio': 100,
    }

    def __init__(self, pattern, type_):
        pattern = quote_plus(re.sub('[{}()\[\]]', '', pattern))
        self.url = u'http://thepiratebay.se/search/%(pattern)s/0/99/%(type)s' % {
            "pattern": pattern,
            "type": self.SEARCH_TYPES[type_]
        }

    def torrents(self):
        doc = get_url_nodes(self.url)
        nodes = doc.select("#searchResult > tbody > tr")
        torrents = []

        for torrent in nodes:
            comments = []
            links = [
                link.get('href')
                for link in torrent.select("a")
                if re.search('magnet:|\.torrent', link.get('href'))
            ]

            torrents.append(Torrent(
                name=torrent.select(".detName")[0].text.strip(),
                links=links,
                seeders_count=int(torrent.select("td")[2].text),
                leechers_count=int(torrent.select("td")[3].text),
                comments=comments
            ))

        return torrents
