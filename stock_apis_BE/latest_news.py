'''
import feedparser
from .models import Article, Category
from dateutil import parser
from django.db import IntegrityError
import time


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
        #art.save()

        try:
            tags = entry['tags']

            for tag in tags:

                try:
                    art.categories.add(Category.objects.get(name=tag['term']))

                except Category.DoesNotExist:
                    cat = Category(name=tag['term'])
                    #cat.save()
                    art.categories.add(cat)

        except KeyError:
            pass

    except IntegrityError:
        pass


def get_latest_articles(website):

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