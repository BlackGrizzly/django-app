from django.shortcuts import render
from django.views.generic import ListView
from .models import Article

class ArticleListView(ListView):
    queryset = Article.objects.defer("content").select_related("author", "category").prefetch_related("tags")
    paginate_by = 10
