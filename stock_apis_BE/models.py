from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
'''
class Post(models.Model):
    name = models.CharField(max_length=200, unique=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return self.name
'''


class Category(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

'''
class Label(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
'''


class Article(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    published_str = models.CharField(max_length=200, null=True)
    published = models.DateTimeField(null=True)
    url = models.TextField()
    categories = models.ManyToManyField(Category)
    #labels = models.ManyToManyField(Label)
    source = models.CharField(max_length=200, default="No source")

    def __str__(self):
        return self.title


