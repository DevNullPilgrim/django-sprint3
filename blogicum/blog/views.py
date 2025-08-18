from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import LAST_FIVE_POSTS
from .models import Category, Post


def get_posts_queryset():
    """Базовый QuerySet для получения опубликованных постов."""
    return (
        Post.objects
        .select_related('author', 'category', 'location')
        .filter(
            is_published=True,
            pub_date__lte=timezone.now(),
        )
        .order_by('-pub_date')
    )


def index(request):
    """Главная: 5 последних постов с валидной и опубликованной категорией."""
    posts = (
        get_posts_queryset()
        .filter(
            category__is_published=True,
        )
        .order_by('-pub_date')[:LAST_FIVE_POSTS]
    )
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, pk):
    """Детальная: пост опубликован, категория существует и опубликована."""
    post = get_object_or_404(
        get_posts_queryset()
        .filter(
            category__is_published=True,
            category__isnull=False
        ),
        pk=pk
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, slug):
    """Лента по категории: сама категория должна быть опубликована."""
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True
    )
    posts = get_posts_queryset().filter(
        category=category).order_by('-pub_date')
    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts,
        'post_list': posts,
    })
