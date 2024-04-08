from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        'Group', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Group(models.Model):
    title = models.CharField(max_length=16)
    slug = models.SlugField(max_length=16)
    description = models.TextField()


class Follow(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following_set'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_set'
    )
