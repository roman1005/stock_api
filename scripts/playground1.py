import json
from string import capwords

from django.http import JsonResponse

from scripts.sources import sources
import feedparser
from dateutil import parser
from django.db import IntegrityError
from django.db.utils import OperationalError
import django
import os
import sys
from stock_apis_BE.categories_aliases import categories_aliases
import requests


os.chdir("..")
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
print(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'stock_apis.settings'
django.setup()

from stock_apis_BE.models import Article

queryset = Article.objects.all().order_by('published')

last = '10000'
ids = []
for query in list(queryset[:int(last)]):
    ids.append(query.id)

print(ids)

queryset = Article.objects.filter(id__in=ids)

print(len(queryset))

category = 'bitcoin'

res_queryset = Article.objects.none()

'''
if category is not None:

    try:
        for cat in categories_aliases[category.lower()]:
            temp_queryset = \
            queryset.filter(categories__name__contains=cat) | \
            queryset.filter(categories__name__contains=cat.lower()) | \
            queryset.filter(categories__name__contains=cat.upper()) | \
            queryset.filter(categories__name__contains=cat.capitalize()) | \
            queryset.filter(categories__name__contains=capwords(cat))

            res_queryset = res_queryset | temp_queryset

    except KeyError:
        res_queryset = \
        queryset.filter(categories__name__contains=category) | \
        queryset.filter(categories__name__contains=category.lower()) | \
        queryset.filter(categories__name__contains=category.upper()) | \
        queryset.filter(categories__name__contains=category.capitalize()) | \
        queryset.filter(categories__name__contains=capwords(category))

    queryset = res_queryset.distinct()

'''
print(len(queryset))

#articles = json.loads\
print(requests.get('http://localhost:8000/v1/articles/', params={'last': 2}).text)

#with open('zalupa.json', 'w') as dump_file:
    #json.dump(articles, dump_file)

text = requests.get('http://127.0.0.1:8000/articles/?last=10').text

with open('list.html', 'w') as f:
    f.write(text)

'''
for query in list(Article.objects.all()[:10]):
    ids.append(query.id)

articles = Article.objects.filter(id__in=ids)

for art in articles:
    for cat in art.categories.all():
        print(cat.name)
'''

for art in Article.objects.all().order_by('-published'):
    temp = art.description.replace('b"', '')
    temp = temp.replace('b\'', '')
    temp = temp.replace('\\n', '')
    temp = ''.join([char if ord(char) < 128 else '' for char in temp])
    temp = temp.replace('\\xe2\\x80\\x99s', '')
    temp = temp.replace('\\xe2\\x80\\x9', '')
    if len(temp) >= 5:
        art.description = temp[:len(temp)-1]
    else:
        art.description = ''
    art.save()
