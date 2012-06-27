# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
from datetime import date
from os import path


def render_resources_as_html(resources, type_):
    render_func = lambda: None

    if type_ == 'video':
        render_func = render_movies_as_html
    elif type_ == 'audio':
        render_func = render_musics_as_html

    return render_func(resources)


def render_movies_as_html(movies):
    current_date = date.today()
    return render_template_as_html('movies.html', {
        'current_date': current_date,
        'movies': movies,
    })


def render_musics_as_html(musics):
    current_date = date.today()
    return render_template_as_html('musics.html', {
        'current_date': current_date,
        'musics': musics,
    })


def render_template_as_html(template, context):
    templates_dir = path.realpath(path.join(path.dirname(__file__), '..', 'templates'))
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template)
    return template.render(**context)
