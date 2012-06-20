#! /usr/bin/env python
# -*- coding: utf-8 -*

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
import re

urls = {
    'this_week': "http://www.imdb.com/movies-in-theaters/",
    'comming_soon': "http://www.imdb.com/movies-coming-soon/",
}


def get_url_nodes(url):
    return BeautifulSoup(urlopen(url).read())


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
            name = torrent.select(".detName")[0].text.strip()
            links = [
                link.get('href')
                for link in torrent.select("a")
                if re.match('magnet:|\.torrent', link.get('href'))
            ]

            torrent_results.append({'name': name, 'links': links})

        return torrent_results


movies = []

for search_type, url in urls.items():
    print "Starting search for %s" % search_type

    try:
        doc = get_url_nodes(url)
        list = doc.select('[itemtype="http://schema.org/Movie"]')

        for item in list:
            try:
                title = item.select('[itemprop="name"]')[0].text
                torrents = PirateBaySearch(title).results()
                movies.append({'title': title, 'piratebay': torrents})
            except:
                next

    except Exception as e:
        print " !!! Fail to get content %s (%s)" % (e.message, type(e).__name__)


print "=" * 100

for movie in movies:
    print movie
    print "-" * 100

print "=" * 100
