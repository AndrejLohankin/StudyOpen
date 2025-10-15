from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


# Кастомный FormSet для проверки наличия одного и только одного основного раздела
class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Считаем количество форм, где is_main = True
        main_count = sum(1 for form in self.forms if form.cleaned_data and form.cleaned_data.get('is_main') and not form.cleaned_data.get('DELETE'))
        # Проверяем, что основной раздел ровно один
        if main_count != 1:
            raise ValidationError('Должен быть выбран ровно один основной раздел.')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset  # Подключаем наш кастомный FormSet
    extra = 1  # Количество пустых форм для добавления новых связей


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    inlines = [ScopeInline]  # Добавляем инлайн для редактирования связей


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']