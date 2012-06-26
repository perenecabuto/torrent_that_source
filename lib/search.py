# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
from model import Torrent, Movie
from model import TorrentSearch, MovieSearch
import re


def get_url_nodes(url):
    return BeautifulSoup(urlopen(url).read())


def for_movies(torrent_search_class, url):
    movies = ImbdSearch(url).movies()

    for movie in movies:
        movie.torrents = torrent_search_class(movie.title).torrents()
    return movies


class ImbdSearch(MovieSearch):

    def __init__(self, url):
        self.url = url

    def movies(self):
        movies = []
        doc = get_url_nodes(self.url)
        list = doc.select('[itemtype="http://schema.org/Movie"]')

        for item in list:
            try:
                movies.append(Movie(
                    title=item.select('[itemprop="name"]')[0].text,
                    image=item.select('[itemprop="image"]')[0].get('src'),
                    synopsis=item.select('[itemprop="description"]')[0].text,
                    genre=", ".join([g.text for g in item.select('[itemprop="genre"]') or []]),
                ))
            except:
                next

        return movies


class PirateBaySearch(TorrentSearch):

    def __init__(self, pattern):
        self.url = u'http://thepiratebay.se/search/'
        self.pattern = pattern

    def search_pattern(self):
        return quote_plus(re.sub('[{}()\[\]\-]', '', self.pattern))

    def torrents(self):
        doc = get_url_nodes(self.url + self.search_pattern())
        nodes = doc.select("#searchResult > tr")
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
