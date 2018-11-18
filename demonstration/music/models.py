from django.contrib.auth.models import Permission, User
import asyncio
from django.db import models
from djincio import MetaDjincio, async_view

class A:
    __metaclass__ = MetaDjincio

class SongQuerySet(models.query.QuerySet):
    def get(self, **kwargs):
        return super().get(**kwargs)
    def all(self, **kwargs):
        return super().all(**kwargs)

class SongManager(models.Manager.from_queryset(SongQuerySet)):
    pass

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)
    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    objects = SongManager()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
