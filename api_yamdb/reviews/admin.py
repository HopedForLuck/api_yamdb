from django.contrib import admin

from .models import Category, Comment, Title, Genre, Review


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


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "text", "score", "pub_date")
    search_fields = ("title", "author")
    list_display_links = ("title",)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.empty_value_display = "Не задано"
