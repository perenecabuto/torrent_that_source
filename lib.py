# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
import re


def get_url_nodes(url):
    return BeautifulSoup(urlopen(url).read())


def search_movies_on_imdb(url):
    movies = []
    doc = get_url_nodes(url)
    list = doc.select('[itemtype="http://schema.org/Movie"]')

    for item in list:
        try:
            title = item.select('[itemprop="name"]')[0].text
            genres = ", ".join([g.text for g in item.select('[itemprop="genre"]') or []])
            movies.append(Movie(
                title=title,
                image=item.select('[itemprop="image"]')[0].get('src'),
                synopsis=item.select('[itemprop="description"]')[0].text,
                genre=genres,
                torrents=PirateBaySearch(title).results()
            ))
        except:
            next

    return movies


class PirateBaySearch(object):

    def __init__(self, title):
        self.url = u'http://thepiratebay.se/search/'
        self.title = title

    @property
    def search_title(self):
        return quote_plus(re.sub('[{}()\[\]\-]', '', self.title))

    def results(self):
        doc = get_url_nodes(self.url + self.search_title)
        torrent_nodes = doc.select("#searchResult > tr")
        torrent_results = []

        for torrent in torrent_nodes:
            comments = []
            links = [
                link.get('href')
                for link in torrent.select("a")
                if re.search('magnet:|\.torrent', link.get('href'))
            ]

            torrent_results.append(Torrent(
                name=torrent.select(".detName")[0].text.strip(),
                links=links,
                seeders_count=int(torrent.select("td")[2].text),
                leechers_count=int(torrent.select("td")[3].text),
                comments=comments
            ))

        return torrent_results


class Torrent(object):
    name = ''
    seeders_count = 0
    leechers_count = 0
    links = []
    comments = []

    def __init__(self, name, links, seeders_count, leechers_count=0, comments=[]):
        self.name = name
        self.links = links
        self.seeders_count = seeders_count
        self.leechers_count = leechers_count
        self.comments = comments


class Movie(object):
    title = ''
    synopsis = ''
    genre = ''
    image = ''
    torrents = []

    def __init__(self, title, genre='', synopsis='', image='', torrents=[]):
        self.title = title
        self.genre = genre
        self.synopsis = synopsis
        self.image = image
        self.torrents = torrents
