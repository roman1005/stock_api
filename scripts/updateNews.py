from scripts.sources import sources, languages
import feedparser
from dateutil import parser
from django.db import IntegrityError
from django.db.utils import OperationalError
import django
import os
import sys
from stock_apis_BE.categories_aliases import categories_aliases

os.chdir("..")
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))


#supported_languages = languages.items()

print(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'stock_apis.settings'
django.setup()

from stock_apis_BE.models import Article, Category
os.chdir("scripts")


last_links = {}


def remove_symbol(string, i):
    before_ith = string[:i]
    after_ith = string[i+1:]
    return before_ith + after_ith

def remove_html_tags(text, open_symb, close_symb):
    
    current_symbol = 0
    inside_tag = 0
    
    for j in range(0, len(text)):
        

        if text[current_symbol] == open_symb:
            text = remove_symbol(text, current_symbol)
            inside_tag += 1

        elif text[current_symbol] == close_symb:
            text = remove_symbol(text, current_symbol)
            inside_tag -= 1

        elif inside_tag > 0:
            text = remove_symbol(text, current_symbol)

        else:
            current_symbol += 1

    return text

def create_article(entry, website, lan):

    try:
        title = entry['title']

    except KeyError:
        title = 'No title'

    try:
        description = remove_html_tags(entry['description'], '<', '>')
        description = remove_html_tags(description, '&', ';')
        description = description.encode("utf-8")
        description = str(description)
        description = description.replace('b"', '')
        description = description.replace('b\'', '')
        description = description.replace('\\n', '')
        description = ''.join([char if ord(char) < 128 else '' for char in description])
        description = description[:len(description)-1]
        description = description.replace('\\xe2\\x80\\x99s', '')
        description = description.replace('\\xe2\\x80\\x9', '')



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
        art = Article.objects.create(title=title, description=description, published=published, published_str=published_str, url=link, source=os.path.dirname(website), language = lan)

        try:
            tags = entry['tags']

            for tag in tags:

                try:
                    art.categories.add(Category.objects.get(name=tag['term']))

                except Category.DoesNotExist:
                    art.categories.create(name=tag['term'])

        except KeyError:
            pass



        #bitcoin_news = Category.objects.get(name='BTC').article_set.all()

        for cat in categories_aliases.keys():

            if (cat in description) or (cat.upper() in description) or (cat[0].upper() + cat[1:].lower()
                                                                        in description) or \
                    (cat in title) or (cat.upper() in title) or (cat[0].upper() + cat[1:].lower() in title):

                for tcat in categories_aliases[cat]:
                    try:
                        temp_cat = Category.objects.get(name=tcat)
                        is_in = art.categories.filter(id=temp_cat.id).count()
                        if is_in < 1:
                            art.categories.add(temp_cat)
                            art.save()
                    except Category.DoesNotExist:
                        art.categories.create(name=cat)
                        art.save()

            try:
                for tcat in categories_aliases[cat]:
                    for tag in tags:
                        if (tcat in tag['term']) or (tcat.upper() in tag['term']) or (tcat[0].upper() + tcat[1:].lower() in tag['term']):

                            try:
                                temp_cat = Category.objects.get(name=cat)
                                if art.categories.filter(name=cat).count() < 1:
                                    art.categories.add(temp_cat)
                                    art.save()

                            except Category.DoesNotExist:
                                art.categories.create(name=cat)
                                art.save()
            except UnboundLocalError:
                pass


        art.save()

    except IntegrityError:
        pass

    except OperationalError as e:
        print(e)
        print(description)
        assert False

def check_for_updates(website):

    feed = feedparser.parse(website + 'rss')

    if len(feed.entries) == 0:
        feed = feedparser.parse(website + 'feed')

    if 'feed' in website:
        feed = feedparser.parse(website)

    last_links[website] = feed.entries

    new_articles = 0

    for entry in last_links[website]:

        try:
            Article.objects.get(title=entry['title'])

        except Article.DoesNotExist:
            print("New article: " + entry['title'])
            try:
                lan = languages[feed['feed']['language']]


            except KeyError:
                lan = 'en'

            create_article(entry, website, lan)


        except Exception as e:
            print(e)

#Article.objects.all().delete()
#Category.objects.all().delete()

'''
for website in sources['crypto']:
    print(website + ": " + str(len(Article.objects.filter(source=website))))
'''

#feed = feedparser.parse('http://feeds.feedburner.com/kryptomoney')
#print("Length: " + str(len(feed.entries)))

#check_for_updates('https://en.cryptonomist.ch/')

'''
for art in Article.objects.all().order_by('-published'):
    print(art.title)
    for cat in categories_aliases.keys():

        if (cat in art.description) or (cat.upper() in art.description) or ((cat[0].upper() + cat[1:].lower()) in art.description) \
                  or (cat in art.title) or (cat.upper() in art.title) or ((cat[0].upper() + cat[1:].lower()) in art.title):

            try:
                temp_cat = Category.objects.get(name=cat)
                if art.categories.filter(name=cat).count() < 1:
                    art.categories.add(temp_cat)
                    art.save()
            except Category.DoesNotExist:
                art.categories.create(name=cat)
                art.save()

        for art_cat in art.categories.all():
            for tcat in categories_aliases[cat]:
                if (tcat in art_cat.name) or (tcat.upper() in art_cat.name) or ((tcat[0].upper() + tcat[1:].lower()) in art_cat.name):

                    try:
                        temp_cat = Category.objects.get(name=tcat)
                        is_in = art.categories.filter(id=temp_cat.id).count()
                        if is_in < 1:
                            art.categories.add(temp_cat)
                            art.save()
                    except Category.DoesNotExist:
                        art.categories.create(name=cat)
                        art.save()
'''


while True:
    '''
    queryset = Article.objects.all().order_by('id')

    if len(queryset) > 9000:
        to_delete = len(queryset) - 9000

        for query in queryset[:to_delete]:
            query.delete()
    '''

    for website in sources:
        print(website.replace('www.', '').replace('.com', '').split('/')[2].upper())
        check_for_updates(website)

