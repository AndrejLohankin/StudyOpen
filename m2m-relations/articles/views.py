from django.shortcuts import render
from django.db.models import Prefetch
from articles.models import Article, Scope


def articles_list(request):
    template = 'articles/news.html'
    articles = Article.objects.prefetch_related(
        Prefetch(
            'scopes',  # related_name из модели Article
            queryset=Scope.objects.select_related('tag').order_by('-is_main', 'tag__name')  # Сортировка
        )
    ).all()

    context = {
        'object_list': articles,
    }

    return render(request, template, context)
