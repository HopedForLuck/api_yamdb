from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Comment, Genre, GenreTitle, Review, Title


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "author",
        "text",
        "pub_date"
    )
    search_fields = ("review",)
    list_filter = ("author",)


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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_display_links = ("name",)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    list_display_links = ("name",)


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("title", "genre",)
    search_fields = ("title", "genre",)
    list_display_links = ("title", "genre",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "text", "score", "pub_date")
    search_fields = ("title", "author")
    list_display_links = ("title",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.empty_value_display = "Не задано"