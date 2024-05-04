from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Quote(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, default=None, null=True
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
