from django.contrib import admin
from .models import Article, Category
from django.db import models

'''
class Search(models.Lookup):
    lookup_name = 'search'

    def as_mysql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return 'MATCH (%s) AGAINST (%s IN BOOLEAN MODE)' % (lhs, rhs), params


models.CharField.register_lookup(Search)
models.TextField.register_lookup(Search)
'''

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    def get_object(self, request, object_id, s):
        # Hook obj for use in formfield_for_manytomany
        self.obj = super(ArticleAdmin, self).get_object(request, object_id)
        # print ("Got object:", self.obj)
        return self.obj

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs["queryset"] = Category.objects.filter(article__id=self.obj.id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    search_fields = ('categories__name', 'title', 'source',)
    exclude = ('published_str',)
    ordering = ('-published',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


# Register your models here.
