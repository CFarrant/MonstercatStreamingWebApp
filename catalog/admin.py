from django.contrib import admin
from django.db import models
from .models import Song, Album, Artist

class AlbumAdmin(admin.ModelAdmin):
  list_display = ('name', 'artist', 'genre_primary', 'genre_secondary', 'release_type', 'release_code')
  list_filter = ('genre_primary', 'genre_secondary', 'release_type')
  pass

class SongAdmin(admin.ModelAdmin):
  list_display = ('title', 'artist', 'album', 'genre_primary', 'genre_secondary')
  list_filter = ('genre_primary', 'genre_secondary')
  pass

admin.site.register(Artist)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)