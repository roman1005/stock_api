from django.contrib import admin
from rest_framework import permissions
from stock_apis.settings import REST_SAFE_LIST_IPS

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

class SafelistPermission(permissions.BasePermission):
    """
    Ensure the request's IP address is on the safe list configured in Django settings.
    """

    def has_permission(self, request, view):

        remote_addr = request.META['REMOTE_ADDR']

        for valid_ip in REST_SAFE_LIST_IPS:
            if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
                return True

        return False
# Register your models here.
