from django.contrib.auth.models import User
from django.db import models

from blog.constants import DEF_RELATED_NAME_POSTS
from blog.service import _short
from core.models import PublishedModel


class Category(PublishedModel):
    """Категория публикации.

    Поля:
        title: Заголовок категории.
        description: Описание категории.
        slug: Уникальный идентификатор для URL.
        is_published: Флаг публикации категории.
        created_at: Автоматическая дата/время создания записи.
    """

    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы латиницы, '
            'цифры, дефис и подчёркивание.'
        )
    )

    class Meta(PublishedModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает читабельное представление категории."""
        return _short(self.title)


class Location(PublishedModel):
    """Местоположение публикации.

    Поля:
        name: Название места.
        is_published: Флаг публикации места.
        created_at: Автоматическое дата/время создания записи.
    """

    name = models.CharField('Название места', max_length=256)

    class Meta(PublishedModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return _short(self.name)


class Post(PublishedModel):
    """Рубликация (пост) пользователя.

    Поля:
        title: Заголовок публикации.
        text: Текст публикации.
        pub_date: Дата и время публикации.
        author: Автор публикации.
        location: Местоположение публикации.
        category: Категория публикации.
        is_published: Флаг публикации.
        created_at: Автоматическая дата/время создания записи.
    """

    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name=DEF_RELATED_NAME_POSTS,

    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name=DEF_RELATED_NAME_POSTS,

    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name=DEF_RELATED_NAME_POSTS,
    )

    class Meta():
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return _short(self.title)
