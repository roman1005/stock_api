from django.contrib import admin
from .models import Article, Category

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
