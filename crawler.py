#! /usr/bin/env python
# -*- coding: utf-8 -*

import yaml
from lib.utils import render_movies_as_html, render_musics_as_html
from lib import search

sources = open("sources.yml", 'r')
content = sources.read()
sources.close()

movies = []
musics = []

# Get data
print "\n\033[01;32m* Crawling data...\033[00m"

for source in yaml.load_all(content):
    print "\033[01;34m* Starting search for %s\033[00m" % source['source']

    try:
        if source['type'] == 'video':
            movies += search.for_movies(search.PirateBaySearch, source)
        elif source['type'] == 'audio':
            musics += search.for_musics(search.PirateBaySearch, source)
    except Exception as e:
        print "! Fail to get content %s (%s)" % (e.message, type(e).__name__)

print ""


# Render html
print "\n\033[01;32m* Generating pages...\033[00m"

if movies:
    render_movies_as_html(movies)

if musics:
    render_musics_as_html(musics)

print "\033[01;34m* Done...\033[00m"
