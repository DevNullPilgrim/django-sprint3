from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """категория публикации.

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
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
        ' цифры, дефис и подчёркивание.'
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ['-created_at']

    def __str__(self):
        """Возвращает читабельное представление категории."""
        return self.title


class Location(models.Model):
    """Местоположение публикации.

    Поля:
        name: Название места.
        is_published: Флаг публикации места.
        created_at: Автоматическое дата/время создания записи.
    """

    name = models.CharField('Название места', max_length=256)
    is_published = models.BooleanField(
        'Опубликовано',
        default=True
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Post(models.Model):
    """Рубликация (пост) пользователя
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
        help_text='Если установить дату и время в будущем — можно делать '
        'отложенные публикации.',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=False, verbose_name='Категория'
    )
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        blank=True
    )
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
