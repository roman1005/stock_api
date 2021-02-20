from rest_framework import serializers
from .models import Article, Category

class CategorySerializer(serializers.Serializer):

    name = serializers.CharField()
    class Meta:
        model = Category

class ArticleSerializer(serializers.Serializer):

    title = serializers.CharField()
    description = serializers.CharField()
    published_str = serializers.CharField()
    published = serializers.DateTimeField()
    categories = CategorySerializer(many=True)
    url = serializers.CharField()
    # labels = serializers.ManyToManyField(Label)
    language = serializers.CharField()
    source = serializers.CharField()
    
    class Meta:
        model = Article
        exclude = ('published_str',)
        depth = 1