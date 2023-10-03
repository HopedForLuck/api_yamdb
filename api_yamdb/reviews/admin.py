from django.contrib import admin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "author",
        "text",
        "pub_date"
    )
    search_fields = ("review",)
    list_filter = ("author",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "category",
    )
    list_editable = (
        "category",
    )
    search_fields = ("name",)
    list_filter = ("category",)
    list_display_links = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_display_links = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_display_links = ("name",)


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("title", "genre",)
    search_fields = ("title", "genre",)
    list_display_links = ("title", "genre",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "text", "score", "pub_date")
    search_fields = ("title", "author")
    list_display_links = ("title",)


admin.site.empty_value_display = "Не задано"
