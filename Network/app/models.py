
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    text = models.TextField()
    time_of_creation = models.DateTimeField(auto_now_add=True)

    # files = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/posts/{self.pk}/'

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:10]

    def accept(self):
        self.status = True
        self.save()

import os

class FileKeep(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/', null=True, blank=True)

    def filename(self):
        return os.path.basename(self.files.name)
    