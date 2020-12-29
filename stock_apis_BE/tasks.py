from __future__ import absolute_import, unicode_literals

import feedparser
#from .models import Article, Category
from dateutil import parser
from django.db import IntegrityError
import time
from celery import shared_task

try:
    print(parser.parse('2020-11-09T06:17:44'))
except parser._parser.ParserError:
    print("Incorrect format")

'''
app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)
'''

'''
@shared_task
def sum(a, b):
    time.sleep(10)
    return a+b

last_links = {}


def make_article(entry, website):

    try:
        title = entry['title']

    except KeyError:
        title = 'No title'

    try:
        description = entry['description']

    except KeyError:
        description = 'No description'

    try:

        published_str = entry['published']
        published = parser.parse(published_str)

    except KeyError:
        published_str = 'No publication date'
        published = None

    try:
        link = entry['link']

    except:
        link = 'No link'

    try:
        art = Article(title=title, description=description, published=published, published_str=published_str, url=link, source=website)
        art.save()

        try:
            tags = entry['tags']

            for tag in tags:

                try:
                    art.categories.add(Category.objects.get(name=tag['term']))

                except Category.DoesNotExist:
                    cat = Category(name=tag['term'])
                    cat.save()
                    art.categories.add(cat)

        except KeyError:
            pass

    except IntegrityError:
        pass

def test(website):

    feed = feedparser.parse(website + 'rss')

    last_links[website] = feed.entries

    new_articles = 0

    for entry in last_links[website]:

        try:
            Article.objects.get(url=entry['link'])

        except Article.DoesNotExist:
            make_article(entry, website)
            new_articles += 1

'''