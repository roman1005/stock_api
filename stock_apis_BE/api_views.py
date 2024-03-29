import json
from datetime import timedelta, datetime
import requests
from django.shortcuts import render
from .models import Article
from rest_framework.views import APIView
from .serializers import ArticleSerializer
from django.http import JsonResponse
from dateutil import parser
from .categories_aliases import categories_aliases
from pyeda.boolalg import expr
from pyeda.parsing.boolexpr import Error as ParseError
from string import capwords
from scripts.sources import shortname_sources
from scripts.sources import supported_languages

class ArticleList(APIView):

    period = None
    key = '856ff040-597a-11eb-80b9-8b2f9f555d46'

    def pyeda_format(self, stri1):

        stri1 = stri1.replace('AND', '&')
        stri1 = stri1.replace('OR', '|')
        stri1 = stri1.replace('NOT ', '~')
        stri1 = stri1.replace('NOT', '~')
        return stri1

    def make_list(self, element):

        res = []
        element = element.replace(')##', '').replace('And(', '')
        for cat in element.split(','):
            if cat[0] == ' ':
                cat = cat[1:]
            res.append(cat)
        return res

    def convert_to_list(self, stri1):

        if stri1 == '':
            return None
        try:
            result1 = str(expr.expr(self.pyeda_format(stri1)).to_dnf())
            result1 = result1.replace('Or(', '').replace('))', ')##').replace('),', ')##,')
            if result1[len(result1)-1] == ')':
                result1 = result1[:len(result1)-1]

            pre_res_list = result1.split(',')

            res_list = []
            current_position = 0

            for i in range(len(pre_res_list)):
                if current_position == len(pre_res_list):
                    break

                if 'And(' in pre_res_list[current_position]:
                    flag = False
                    new_str = pre_res_list[current_position]
                    current_position += 1
                    while not flag:
                        if current_position == len(pre_res_list):
                            break

                        new_str += ',' + pre_res_list[current_position]
                        if ')##' in pre_res_list[current_position]:
                            flag = True
                        else:
                            current_position += 1

                    res_list.append(new_str)
                    # print(res_list)

                else:
                    if not (')##' in pre_res_list[current_position]):
                        res_list.append(pre_res_list[current_position])
                    current_position += 1

            for i, element in enumerate(res_list):
                if res_list[i][0] == ' ':
                    res_list[i] = res_list[i][1:]

                if 'And' in element:
                    res_list[i] = self.make_list(element)

            return res_list

        except ParseError as e:
            error_msg = str(e)
            error_msg = error_msg.replace('&', 'AND')
            error_msg = error_msg.replace('|', 'OR')
            error_msg = error_msg.replace('~', 'NOT')
            # error_msg = error_msg.replace('NOT', '~')
            print(error_msg)
            raise ParseError(error_msg)

    def get_articles(self, query):

        queryset = Article.objects.all().order_by('-published')

        res_queryset = Article.objects.none()

        if query is not None:

            temp_query = query.replace('~', '')

            try:
                for cat in categories_aliases[temp_query.lower()]:
                    temp_queryset = \
                        queryset.filter(categories__name__contains=cat) | \
                        queryset.filter(categories__name__contains=cat.lower()) | \
                        queryset.filter(categories__name__contains=cat.upper()) | \
                        queryset.filter(categories__name__contains=cat.capitalize()) | \
                        queryset.filter(categories__name__contains=capwords(cat))

                    res_queryset = res_queryset | temp_queryset

            except KeyError:
                res_queryset = \
                    queryset.filter(categories__name__contains=temp_query) | \
                    queryset.filter(categories__name__contains=temp_query.lower()) | \
                    queryset.filter(categories__name__contains=temp_query.upper()) | \
                    queryset.filter(categories__name__contains=temp_query.capitalize()) | \
                    queryset.filter(categories__name__contains=capwords(temp_query))

        if query[0] == '~':
            result = Article.objects.exclude(pk__in=res_queryset.values_list('pk', flat=True))
        else:
            result = res_queryset

        return result.distinct()

    def make_forms(self, word):
        return [word.lower(), word.upper(), capwords(word)]

    def get_queryset(self, result):

        if result is None:
            return Article.objects.none()

        queryset = Article.objects.none()

        for query_list in result:

            if type(query_list) == str:
                queryset = queryset | self.get_articles(query_list)
            elif type(query_list) == list:
                sub_queryset = Article.objects.all()
                for query in query_list:
                    sub_queryset = sub_queryset.distinct() & self.get_articles(query)

                queryset = queryset | sub_queryset

        return queryset.distinct().order_by('-published')

    def get_by_sources(self, sources, procedure):
        if sources is not None:
            source_list = sources.split(',')
            for i, source in enumerate(source_list):
                source_list[i] = source.replace(' ', '')

            temp_queryset = Article.objects.none()

            for source in source_list:
                try:
                    temp_queryset = temp_queryset | Article.objects.filter(source=shortname_sources[source])
                except KeyError:
                    return JsonResponse(status=400, data={'status':'400', 'message': 'Source ' + source + ' is not an provided source.'} )

            return temp_queryset.distinct()
        elif procedure == 'include':
            return Article.objects.all().distinct()
        elif procedure == 'exclude':
            return Article.objects.none()

    def get_by_languages(self, languages):

        languages_list = languages.split(',')
        queryset = Article.objects.none()
        for language in languages_list:
            if language is not (None or ''):
                if language in supported_languages:
                    queryset = queryset | Article.objects.filter(language=language)
                else:
                    return JsonResponse(status=400, data={'status':'400', 'message': 'Not supported language was requested'})

        return queryset.distinct()

    def search_by_words(self, words, field='title', procedure='include'):
        if words is not None:
            word_list = words.split(',')
            for i, source in enumerate(word_list):
                word_list[i] = source.replace(' ', '')

            if procedure == 'include':
                temp_queryset = Article.objects.all()
                for word in word_list:
                    temp_temp_queryset = Article.objects.none()

                    for word_form in self.make_forms(word):
                        if field == 'title' and procedure == 'include':
                            temp_temp_queryset = temp_temp_queryset | Article.objects.filter(title__contains=word_form)
                        elif field == 'description' and procedure == 'include':
                            temp_temp_queryset = temp_temp_queryset | Article.objects.filter(description__contains=word_form)
                    temp_queryset = temp_queryset & temp_temp_queryset

            elif procedure == 'exclude':
                temp_queryset = Article.objects.none()
                for word in word_list:
                    for word_form in self.make_forms(word):
                        if field == 'title':
                            temp_queryset = temp_queryset | Article.objects.filter(title__contains=word_form)
                        elif field == 'description':
                            temp_queryset = temp_queryset | Article.objects.filter(description__contains=word_form)

            return temp_queryset.distinct()

        elif procedure == 'include':
            return Article.objects.all().distinct()
        elif procedure == 'exclude':
            return Article.objects.none()

    def get(self, request, **kwargs):

        try:
            self.period = self.kwargs['period']
        except KeyError:
            pass

        headers = request.headers

        try:
            if headers['X-RapidAPI-Proxy-Secret'] != self.key:
                return JsonResponse(status=400, data={'status':'400', 'message': "Invalid credentials were provided."})
        except KeyError:
            return JsonResponse(status=400, data={'status':'400', 'message': "Invalid credentials were provided."})

        '''
        remote_addr = request.META['REMOTE_ADDR']
        for valid_ip in settings.REST_SAFE_LIST_IPS:

            if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
                break
            else:
                return JsonResponse(status=400, data={'status':'400', 'message': "Not verified IP."})
        '''

        category = self.request.query_params.get('category', None)
        queryset = Article.objects.all()

        if category is not None:
            queryset = self.get_queryset(self.convert_to_list(category))
        else:
            queryset = Article.objects.all()

        if self.period == 'day' or self.period == 'week':

            to_datetime_str = self.request.query_params.get('ending_at', None)

            if to_datetime_str is None:
                to_datetime = datetime.now()

            else:
                try:
                    to_datetime = parser.parse(to_datetime_str)

                except parser._parser.ParserError:
                    return JsonResponse(status=400, data={'status':'400', 'message': "Incorrect data format was inputted"})

            if self.period == 'day':
                from_datetime = to_datetime - timedelta(days=1)
            elif self.period == 'week':
                from_datetime = to_datetime - timedelta(days=7)

            queryset = queryset.filter(published__gte=from_datetime)
            queryset = queryset.filter(published__lte=to_datetime)

        '''
        if from_date_str is not None:
            try:
                from_date = parser.parse(from_date_str)
                queryset = queryset.filter(published__gte=from_date)

            except parser._parser.ParserError:
                return JsonResponse(status=400, data={'status':'400', 'message': "Incorrect data format was inputted"})

        if to_date_str is not None:

            try:
                to_date = parser.parse(to_date_str)
                queryset = queryset.filter(published__lte=to_date)

            except parser._parser.ParserError:
                return JsonResponse(status=400, data={'status':'400', 'message': "Incorrect data format was inputted"})
        '''


        sources = self.request.query_params.get('includeSources', None)
        queryset = queryset.distinct() & self.get_by_sources(sources, 'include')

        sources = self.request.query_params.get('excludeSources', None)
        exclude_sources_queryset = self.get_by_sources(sources, 'exclude')
        queryset = queryset.distinct() & Article.objects.exclude(pk__in=exclude_sources_queryset.values_list('pk', flat=True)).distinct()

        include_words_title = self.request.query_params.get('includeWordsTitle', None)
        queryset = queryset.distinct() & self.search_by_words(include_words_title, 'title', 'include')

        exclude_words_title = self.request.query_params.get('excludeWordsTitle', None)
        exclude_words_queryset = self.search_by_words(exclude_words_title, 'title', 'exclude')
        queryset = queryset.distinct() & Article.objects.exclude(pk__in=exclude_words_queryset.values_list('pk', flat=True)).distinct()

        include_words_title = self.request.query_params.get('includeWordsDescription', None)
        queryset = queryset.distinct() & self.search_by_words(include_words_title, 'description', 'include')

        exclude_words_title = self.request.query_params.get('excludeWordsDescription', None)
        exclude_words_queryset = self.search_by_words(exclude_words_title, 'description', 'exclude')
        queryset = queryset.distinct() & Article.objects.exclude(pk__in=exclude_words_queryset.values_list('pk', flat=True)).distinct()

        languages = self.request.query_params.get('languages', None)

        if languages is not None:
            try:
                result = self.get_by_languages(languages)
                queryset &= result
            except AttributeError:
                return result

        last = self.request.query_params.get('last', None)

        if last is not None:
            try:
                int_last = int(last)
                if str(int_last) != last:
                    return JsonResponse(status=400, data={'status':'400', 'message': "Incorrect parameter value - you should enter only positive integer numbers."})
            except ValueError:
                return JsonResponse(status=400, data={'status':'400', 'message': "Incorrect parameter value - you should enter only positive integer numbers."})

            last_val = int(last)

            try:
                ids = []

                if last_val > 1000 and len(queryset) > 1000:
                    return JsonResponse(status=400, data={'status':'400', 'message': "You can get only up to 1000 last articles for one request."})

                for query in queryset.order_by('-published')[:last_val]:
                    ids.append(query.id)


            except AssertionError:
                return JsonResponse(status=400, data={'status':'400', 'message': "Incorrect parameter value - you should enter only positive integer numbers."})

            queryset = Article.objects.filter(id__in=ids).order_by('-published')
        else:
            ids = []
            for query in queryset.order_by('-published')[:1000]:
                ids.append(query.id)
            queryset = Article.objects.filter(id__in=ids).order_by('-published')

        order_by = self.request.query_params.get('orderBy', None)

        if order_by is None:
            serializer = ArticleSerializer(queryset.order_by('-published'), many=True)
            return JsonResponse({"results": len(queryset), "articles": serializer.data})
        else:
            try:
                serializer = ArticleSerializer(queryset.order_by(order_by), many=True)
                return JsonResponse({"results": len(queryset), "articles": serializer.data})
            except Exception as er:
                raise Exception(er)


class SourceList(APIView):

    def get(self, request):

        headers = request.headers
        '''
        try:
            if headers['X-RapidAPI-Proxy-Secret'] != '856ff040-597a-11eb-80b9-8b2f9f555d46':
                return JsonResponse(status=400, data={'status':'400', 'message': "Invalid credentials were provided."})
        except KeyError:
            return JsonResponse(status=400, data={'status':'400', 'message': "Invalid credentials were provided."})
        '''

        return JsonResponse(shortname_sources)


def articles_html(request, **kwargs):
    period = kwargs['period']
    if period=='week' or period=='day':
        api_request = request.build_absolute_uri().replace(f'articles/{period}', f'v1/articles/{period}')
    else:
        return JsonResponse(status=400, data={'status':'400', 'message': f"Unprovided endpoint: '{period}', should be 'week' or 'day'"})

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
