from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import Comment, Post


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_post')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('id', 'header', 'text', 'picture', 'from_user', 'button')

    def button(self):
        return format_html(f'<a class="button" href="{reverse("admin:delcoms", args=[self.id])}">Delete comments</a>')

    def get_urls(self):
        urls = super().get_urls()
        shard_urls = [path('delcoms/<_id>', self.admin_site.admin_view(self.delete_comments), name="delcoms"), ]
        return shard_urls + urls

    @staticmethod
    def delete_comments(self, arg, _id):
        Comment.objects.filter(to_post=_id).delete()
        return redirect(reverse('admin:main_post_changelist'))
