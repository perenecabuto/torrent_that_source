#! /usr/bin/env python
# -*- coding: utf-8 -*

from lib.utils import render_movies_as_html
from lib import search

urls = (
    ('comming_soon', "http://www.imdb.com/movies-coming-soon/"),
    ('this_week', "http://www.imdb.com/movies-in-theaters/"),
)

movies = []

# Get data
print "\n\033[01;32m* Crawling data...\033[00m"

for search_type, url in urls:
    print "\033[01;34m* Starting search for %s\033[00m" % search_type

    try:
        movies += search.for_movies(search.PirateBaySearch, url)
    except Exception as e:
        print "! Fail to get content %s (%s)" % (e.message, type(e).__name__)

print ""


# Render html
print "\n\033[01;32m* Generating pages...\033[00m"

render_movies_as_html(movies)

print "\033[01;34m* Done...\033[00m"
