from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "publish", "status")
    search_fields = ["title", "author", "body"]
    list_filter = ["created", "updated", "status"]
    date_hierarchy = "publish"
    prepopulated_fields = {"slug": ("title",)}
