# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urllib import quote_plus
from model import Torrent, Video, Audio
from model import TorrentSearch, ResourceSearch
import re


def get_url_nodes(url):
    return BeautifulSoup(urlopen(url).read())


def for_resources(torrent_search_class, source):
    resource_search_class = None

    if source['type'] == 'video':
        resource_search_class = VideoSearch
    elif source['type'] == 'audio':
        resource_search_class = AudioSearch

    resources = resource_search_class(source).items()

    for r in resources:
        r.torrents = torrent_search_class(r.search_terms(), source['type']).torrents()

    return resources


def get_resource_nodes(url, selector, callback):
    items = []
    doc = get_url_nodes(url)

    for node in doc.select(selector.text):
        try:
            items.append(callback(node))
        except:
            next

    return items


def subnode_by_selector(node, selector):
    return node.select(selector.text)[selector.pos]


def subnodes_by_selector(node, selector):
    return node.select(selector.text)


class Selector(object):
    text = ''
    pos = 0

    def __init__(self, str_or_list_or_dict):
        if type(str_or_list_or_dict) is list:
            self.text = str_or_list_or_dict[0]
            self.pos = str_or_list_or_dict[1]

        if type(str_or_list_or_dict) is dict:
            self.text = str_or_list_or_dict.get('selector', self.text)
            self.pos = str_or_list_or_dict.get('position', self.pos)

        if type(str_or_list_or_dict) is str:
            self.text = str_or_list_or_dict


class VideoSearch(ResourceSearch):

    def __init__(self, source):
        self.url = source['url']
        self.items_selector = Selector(source['items_selector'])
        self.title_selector = Selector(source['title_selector'])
        self.genre_selector = Selector(source['genre_selector'])
        self.image_selector = Selector(source['image_selector'])
        self.synopsis_selector = Selector(source['synopsis_selector'])

    def items(self):
        return get_resource_nodes(
            self.url,
            self.items_selector,
            lambda node: Video(
                title=subnode_by_selector(node, self.title_selector).text,
                image=subnode_by_selector(node, self.image_selector).get('src'),
                synopsis=subnode_by_selector(node, self.synopsis_selector).text,
                genre=", ".join([g.text for g in subnodes_by_selector(node, self.genre_selector) or []]),
            )
        )


class AudioSearch(ResourceSearch):

    def __init__(self, source):
        self.url = source['url']
        self.items_selector = Selector(source['items_selector'])
        self.name_selector = Selector(source['name_selector'])
        self.artist_selector = Selector(source['artist_selector'])
        self.label_selector = Selector(source['label_selector'])

    def items(self):
        return get_resource_nodes(
            self.url,
            self.items_selector,
            lambda node: Audio(
                title=subnode_by_selector(node, self.name_selector).text.strip(),
                artist=subnode_by_selector(node, self.artist_selector).text.strip(),
                label=subnode_by_selector(node, self.label_selector).text.strip()
            )
        )


class PirateBaySearch(TorrentSearch):
    SEARCH_TYPES = {
        'video': 200,
        'audio': 100,
    }

    def __init__(self, pattern, type_):
        pattern = quote_plus(re.sub('[{}()\[\]]', '', pattern))
        self.url = u'http://thepiratebay.se/search/%(pattern)s/0/7/%(type)s' % {
            "pattern": pattern,
            "type": self.SEARCH_TYPES[type_]
        }

    def torrents(self):
        doc = get_url_nodes(self.url)
        nodes = doc.select("#searchResult > tr")[1:]
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
