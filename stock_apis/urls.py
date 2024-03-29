"""stock_apis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from stock_apis_BE.api_views import ArticleList, articles_html, SourceList

urlpatterns = [
    path('articles/<period>/', articles_html, name='articles'),
    url(r'', admin.site.urls),
    path('admin/', admin.site.urls),
    path('v1/articles/week/', ArticleList.as_view(), {'period': 'week'}),
    path('v1/articles/day/', ArticleList.as_view(), {'period': 'day'}),
    path('v1/articles/', ArticleList.as_view()),
    path('v1/sources/all/', SourceList.as_view())
]
