from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']  # Сортировка по алфавиту по умолчанию

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name='Изображение')

    # Связь многие-ко-многим с Tag через промежуточную модель Scope
    tags = models.ManyToManyField(Tag, through='Scope', related_name='articles', verbose_name='Разделы')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']  # Сортировка по дате публикации (новые первыми)

    def __str__(self):
        return self.title


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name='Статья')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes', verbose_name='Раздел')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статей'
        # Уникальность пары article-tag, чтобы не было дубликатов
        unique_together = ('article', 'tag')

    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"