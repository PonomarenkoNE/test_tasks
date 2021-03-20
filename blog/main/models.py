from django.db import models
from django.shortcuts import redirect
from django.contrib.auth.models import User


class Post(models.Model):

    from_user = models.ForeignKey(User, related_name='user_posted', on_delete=models.CASCADE)
    header = models.CharField(max_length=20)
    picture = models.ImageField(upload_to='media', blank=True, null=True)
    text = models.TextField()

    class Meta():
        verbose_name = "Post"
        verbose_name_plural = "Posts"


class Comment(models.Model):

    from_user = models.ForeignKey(User, related_name='user_commented', on_delete=models.CASCADE)
    text = models.TextField()
    to_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta():
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
