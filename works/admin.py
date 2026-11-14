from django.contrib import admin
from .models import Category, Order, Post, Profile, Project, SocialLink

admin.site.site_header = "مدیریت سایت نمونه‌کار"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "order", "created")
    list_filter = ("category", "featured")
    search_fields = ("title", "summary", "tags")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order")


admin.site.register(Profile)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "created")
    list_filter = ("published",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "contact", "handled", "created")
    list_filter = ("kind", "handled")
    list_editable = ("handled",)
    search_fields = ("name", "contact", "message")
