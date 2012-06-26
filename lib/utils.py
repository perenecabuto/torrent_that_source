# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
from datetime import date
from os import path


def render_movies_as_html(movies):
    templates_dir = path.realpath(path.join(path.dirname(__file__), '..', 'templates'))
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('movies.html')
    current_date = date.today()
    static_filename = (current_date.strftime('%Y%m%d'), 'movies-index.html')
    index = open('static/%s-%s' % static_filename, 'w')

    index.write(template.render(movies=movies, current_date=current_date))
    index.close()


def render_musics_as_html(musics):
    templates_dir = path.realpath(path.join(path.dirname(__file__), '..', 'templates'))
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('musics.html')
    current_date = date.today()
    static_filename = (current_date.strftime('%Y%m%d'), 'musics-index.html')
    index = open('static/%s-%s' % static_filename, 'w')

    index.write(template.render(musics=musics, current_date=current_date))
    index.close()
