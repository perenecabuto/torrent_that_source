#! /usr/bin/env python
# -*- coding: utf-8 -*

from datetime import date
from lib import search_movies_on_imdb

urls = {
    'this_week': "http://www.imdb.com/movies-in-theaters/",
    'comming_soon': "http://www.imdb.com/movies-coming-soon/",
}

movies = []

print "\n* Crawling data...", "\n ", "-" * 100

for search_type, url in urls.items():
    print "- Starting search for %s" % search_type

    try:
        movies += search_movies_on_imdb(url)
    except Exception as e:
        print "! Fail to get content %s (%s)" % (e.message, type(e).__name__)


print "\n * Generating pages...", "\n ", "-" * 100

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('index.html')

current_date = date.today()
static_filename = (current_date.strftime('%Y%m%d'), 'index.html')
index = open('static/%s-%s' % static_filename, 'w')

index.write(
    template.render(
      movies=movies,
      current_date=current_date,
    )
)

index.close()
print ""
