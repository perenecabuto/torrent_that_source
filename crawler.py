#! /usr/bin/env python
# -*- coding: utf-8 -*

import yaml
from lib import utils
from lib import search
from datetime import date

sources = open("sources.yml", 'r')
content = sources.read()
sources.close()

for conf in yaml.load(content)['sources']:
    try:
        print "\033[01;32m* Crawling data for %s\033[00m" % conf['source']
        resources = search.for_resources(search.PirateBaySearch, conf)

        # Render html
        print "\033[01;34m* Generating pages...\033[00m"
        page_content = utils.render_resources_as_html(resources, conf['type'])

        output_path = 'static/%(source)s-%(type)s-%(date)s.html' % {
            'source': conf['source'],
            'type': conf['type'],
            'date': date.today().strftime('%Y%m%d'),
        }

        index = open(output_path, 'w')
        index.write(page_content)
        index.close()
        print "\033[01;34m* Done...\033[00m\n"

    except Exception as e:
        print "! Fail to get content %s (%s)" % (e.message, type(e).__name__)
