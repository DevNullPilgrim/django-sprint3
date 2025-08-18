from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category, Location


def index(request):
    """Главная страница блога.

    Отображает 5 последних опубликованных постов.
    - is_published: Флаг публикации поста.
    - pub_date <= текущее время.
    - категория публикации не пуста.

    """
    now = timezone.now()
    posts = (
        Post.objects
        .filter(
            is_published=True,
            pub_date__lte=now,
            category__is_published=True,
            category__isnull=False
        )
        .select_related('author', 'category', 'location')
        .order_by('-pub_date')[:5]
    )
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, pk):
    """
    Детальная страница поста.

    Условия для 404:
    - пост не опубликован
    - pub_date в будущем
    - категория не опубликована или отсутствует
    """
    now = timezone.now()
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location'),
        pk=pk,
        is_published=True,
        pub_date__lte=now,
        category__is_published=True,
        category__isnull=False
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, slug):
    """
    Страница категории.

    Условия для 404:
    - категория не опубликована или отсутствует

    Посты:
    - только опубликованные,
    - с pub_date <= текущее время,
    - принадлежат этой категории.
    """
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = (
        category.post_set
        .filter(
            category=category,
            is_published=True,
            pub_date__lte=timezone.now()
        ).select_related(
            'author',
            'category',
            'location'
        ).order_by(
            '-pub_date'
        )
    )
    return render(
        request, 'blog/category.html', {
            'category': category,
            'posts': posts,
            'post_list': posts
        }
    )


def location_posts(request, slug):
    """
    Страница метоположения.

    Условия для 404:
    - метоположения не опубликована или отсутствует.

    Посты:
    - только опубликованные,
    - с pub_date <= текущее время,
    - принадлежат этому местоположению.
    """
    location = get_object_or_404(Location, slug=slug)
    posts = (Post.objects.filter(is_published=True, location=location)
             .select_related('author', 'category', 'location')
             .order_by('-pub_date'))
    return render(request, 'blog/location.html', {
        'location': location,
        'posts': posts
    }
    )
