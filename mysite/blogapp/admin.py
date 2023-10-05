from typing import Any
from django.db.models import QuerySet
from django.contrib import admin
from django.http import HttpRequest
from .models import Article, Author, Category, Tag

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

class TagInline(admin.TabularInline):
    model = Article.tags.through

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "pub_date", "author", "category"
    inlines = [
        TagInline,
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return Article.objects.select_related("author", "category").prefetch_related("tags")