from django.shortcuts import render
from django.db.models import Prefetch
from articles.models import Article, Scope


def articles_list(request):
    template = 'articles/news.html'

    # Используем prefetch_related с Prefetch для отсортированных scopes
    # Важно: используем select_related('tag'), чтобы загрузить связанный тег
    # и затем сортируем по is_main (убывание) и по имени тега (возрастание)
    articles = Article.objects.prefetch_related(
        Prefetch(
            'scopes',  # related_name из модели Article
            queryset=Scope.objects.select_related('tag').order_by('-is_main', 'tag__name')  # Сортировка
        )
    ).all()

    # Передаём статьи под именем 'object_list', которое использует шаблон
    context = {
        'object_list': articles,
    }

    return render(request, template, context)