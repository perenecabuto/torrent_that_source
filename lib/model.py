# -*- coding: utf-8 -*-


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


class Video(object):
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

    def search_terms(self):
        return self.title


class Audio(object):
    title = ''
    artist = ''
    label = ''
    torrents = []

    def __init__(self, title, artist='', label='', torrents=[]):
        self.title = title.encode('utf-8')
        self.artist = artist.encode('utf-8')
        self.label = label.encode('utf-8')
        self.torrents = torrents

    def search_terms(self):
        return '%s - %s' % (self.title, self.artist)


class TorrentSearch(object):

    def __init__(self, pattern):
        """
        It must have a url and a pattern
        """
        raise NotImplemented("__init__")

    def search_pattern(self):
        """
        It must returns a string with the parsed and cleaned pattern attribute,
        optimized for resource best response.
        """
        raise NotImplemented("search_pattern")

    def torrents(self):
        """
        It must returns a list of Torrent objects as the result
        of the data gotten from the resource
        """
        raise NotImplemented("results")


class ResourceSearch(object):

    def __init__(self, url):
        """
        It must have a url and a pattern
        """
        raise NotImplemented("__init__")

    def items(self):
        """
        It must returns a list of Video objects as the result
        of the data gotten from the resource
        """
        raise NotImplemented("results")
