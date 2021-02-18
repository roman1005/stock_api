import os
import sys
from string import capwords

import django
from pyeda.boolalg import expr
from pyeda.parsing.boolexpr import Error as ParseError

from stock_apis_BE.categories_aliases import categories_aliases

os.chdir("..")
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
print(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE'] = 'stock_apis.settings'
django.setup()


from stock_apis_BE.models import Article


def pyeda_format(stri1):
    stri1 = stri1.replace('AND', '&')
    stri1 = stri1.replace('OR', '|')
    stri1 = stri1.replace('NOT ', '~')
    stri1 = stri1.replace('NOT', '~')
    return stri1


def make_list(element):

    res = []
    element = element.replace(')##', '').replace('And(', '')
    for cat in element.split(','):
        if cat[0] == ' ':
            cat = cat[1:]
        res.append(cat)
    return res


def convert_to_list(stri1):

    if stri1 == '':
        return None
    try:
        result1 = str(expr.expr(pyeda_format(stri1)).to_dnf())
        result1 = result1.replace('Or(', '').replace('))', ')##').replace('),', ')##,')

        if result1[len(result1) - 1] == ')':
            result1 = result1[:len(result1) - 1]

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

                    new_str += ','+ pre_res_list[current_position]
                    if ')##' in pre_res_list[current_position]:
                        flag = True
                    else:
                        current_position += 1

                res_list.append(new_str)
                #print(res_list)

            else:
                if not (')##' in pre_res_list[current_position]):
                    res_list.append(pre_res_list[current_position])
                current_position += 1

        for i, element in enumerate(res_list):
            if res_list[i][0] == ' ':
                res_list[i] = res_list[i][1:]

            if 'And' in element:
                res_list[i] = make_list(element)

        return res_list

    except ParseError as e:
        error_msg = str(e)
        error_msg = error_msg.replace('&', 'AND')
        error_msg = error_msg.replace('|', 'OR')
        error_msg = error_msg.replace('~', 'NOT')
        #error_msg = error_msg.replace('NOT', '~')
        print(error_msg)
        return ParseError(error_msg)


def get_articles(query):

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


def get_queryset(result):

    if result is None:
        return Article.objects.none()

    queryset = Article.objects.none()

    for query_list in result:

        if type(query_list) == str:
            queryset = queryset | get_articles(query_list)
        elif type(query_list) == list:
            sub_queryset = Article.objects.all()
            for query in query_list:
                sub_queryset = sub_queryset.distinct() & get_articles(query)

            queryset = queryset | sub_queryset

    return queryset.distinct()


#stri1 = '(NOT(bitcoin AND litecoin AND cardano)) OR ((NOT monero OR litecoin AND bitcoin) AND (cardano OR ethereum))'
stri1 = 'NOT bitcoin'
result = convert_to_list(stri1)
print(result)
print(len(get_queryset(result)))

stri2 = '(NOT(bitcoin AND AND litecoin)) OR ((NOT monero OR litecoin) AND (cardano OR ethereum))'
result = convert_to_list(stri2)






