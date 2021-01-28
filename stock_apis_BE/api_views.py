import json
import os

from stock_apis import settings
from .categories_aliases import categories_aliases
import feedparser
import requests
from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Article
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from dateutil import parser
from .categories_aliases import categories_aliases
from string import capwords

class ArticleList(APIView):

    def get(self, request):

        if self.request.query_params.get('X-RapidAPI-Proxy-Secret') != '856ff040-597a-11eb-80b9-8b2f9f555d46':
            raise Exception("Invalid credentials were provided.")

        remote_addr = request.META['REMOTE_ADDR']

        for valid_ip in settings.REST_SAFE_LIST_IPS:

            if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
                break
            else:
                raise Exception("Not verified IP.")

        queryset = Article.objects.all().order_by('-published')

        category = self.request.query_params.get('category', None)

        res_queryset = Article.objects.none()


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

            queryset = res_queryset.distinct().order_by('-published')

        from_date_str = self.request.query_params.get('from', None)
        to_date_str = self.request.query_params.get('to', None)

        if from_date_str is not None:

            try:
                from_date = parser.parse(from_date_str)
                queryset = queryset.filter(published__gte=from_date)

            except parser._parser.ParserError:
                raise Exception("Incorrect data format was inputted")

        if to_date_str is not None:

            try:
                to_date = parser.parse(to_date_str)
                queryset = queryset.filter(published__lte=to_date)

            except parser._parser.ParserError:
                raise Exception("Incorrect data format was inputted")

        last = self.request.query_params.get('last', None)

        if last is not None:
            try:
                ids = []
                for query in queryset[:int(last)]:
                    ids.append(query.id)

                queryset = Article.objects.filter(id__in=ids).order_by('-published')


            except:
                raise Exception("Incorrect parameter value - you should enter only positive integer numbers.")

        serializer = ArticleSerializer(queryset, many=True)

        return JsonResponse({"results": len(queryset), "articles": serializer.data})


def articles_html(request):
    api_request = request.build_absolute_uri().replace('articles/', 'v1/articles')
    articles = json.loads(requests.get(api_request).text)['articles']

    context = {}

    for art in articles:
        is_coin = False
        temp_cats = []
        for cat in art['categories']:
            A = cat['name'] in ['Bitcoin', 'Litecoin', 'Monero', 'Ethereum', 'Ripple', 'Cardano', 'BTC', 'LTC', 'ETH', 'XMR', 'XRP', 'CARD']
            B = cat['name'][0].upper() + cat['name'][1:] in ['Bitcoin', 'Litecoin', 'Monero', 'Ethereum', 'Ripple', 'Cardano', 'BTC', 'LTC', 'ETH', 'XMR', 'XRP', 'CARD']
            C = cat['name'].upper() in ['Bitcoin', 'Litecoin', 'Monero', 'Ethereum', 'Ripple', 'Cardano', 'BTC', 'LTC', 'ETH', 'XMR', 'XRP', 'CARD']
            if A or B or C:

                tcat=categories_aliases[cat['name'].lower()][1]

                if tcat.upper() not in temp_cats:
                    temp_cats.append(tcat.upper())
                    is_coin = True

        if not is_coin:
            temp_cats.append('CRYPTO')

        art['categories'] = temp_cats

    colors = {'BTC': '#efa80a', 'ETH': '#1cfaf4', 'LTC': '#d900ff', 'XMR': '#ff0028', 'XRP': '#1cff00', 'CARD': '#ffe544', 'CRYPTO': '#a26060'}

    context['articles'] = articles
    context['colors'] = colors

    return render(request, 'base.html', context)
    #return HttpResponse(api_request)
