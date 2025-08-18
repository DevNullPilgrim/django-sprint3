from django.contrib import admin, messages
from django.contrib.auth.models import Group

from .constants import ADMIN_LIST_PER_PAGE
from .forms import GroupForm
from .models import Category, Location, Post

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Кастомная админка для Group с упрощённым виджетом прав."""

    form = GroupForm


@admin.action(description="Опубликовать выбранные объекты")
def mark_published(modeladmin, request, queryset):
    """Массово включает is_published у выбранных объектов."""
    updated = queryset.update(is_published=True)
    modeladmin.message_user(
        request, f'Опубликовано: {updated}', level=messages.SUCCESS)


@admin.action(description="Снять с публикации выбранные объекты")
def mark_unpublished(modeladmin, request, queryset):
    """Массово выключает is_published у выбранных объектов."""
    updated = queryset.update(is_published=False)
    modeladmin.message_user(
        request, f'Снято с публикации: {updated}', level=messages.SUCCESS)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории: быстрый доступ к публикации, автослаг, поиск/фильтры."""

    list_display = ("id", "title", "slug", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)
    ordering = ("title",)
    list_per_page = ADMIN_LIST_PER_PAGE
    actions = [mark_published, mark_unpublished]
    actions_on_bottom = True


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Локации: та же схема, что и у категорий."""

    list_display = ("id", "name", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("name",)
    readonly_fields = ("created_at",)
    ordering = ("name",)
    list_per_page = ADMIN_LIST_PER_PAGE
    actions = [mark_published, mark_unpublished]
    actions_on_bottom = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админка публикаций.

    Фильтры, поиск, быстрая правка; иерархия по дате.
    """

    list_display = (
        "id", "title", "author", "category", "location",
        "is_published", "pub_date", "created_at",
    )
    list_filter = ("is_published", "category", "location", "pub_date")
    list_editable = ("is_published",)
    search_fields = ("title", "text", "author__username")
    date_hierarchy = "pub_date"
    ordering = ("-pub_date",)
    readonly_fields = ("created_at",)
    list_select_related = ("author", "category", "location")
    autocomplete_fields = ("author", "category", "location")
    save_on_top = True
    list_per_page = ADMIN_LIST_PER_PAGE
    actions = [mark_published, mark_unpublished]
    actions_on_bottom = True

    fieldsets = (
        ("Основное", {"fields": ("title", "text")}),
        ("Связи и публикация", {
            "fields": (
                "author",
                "category",
                "location",
                "is_published",
                "pub_date"),
        }),
        ("Служебные", {"fields": ("created_at",)}),
    )


admin.site.site_header = "Администрирование блога"
admin.site.site_title = "Blogicum — Админка"
admin.site.index_title = "Управление блогом"
