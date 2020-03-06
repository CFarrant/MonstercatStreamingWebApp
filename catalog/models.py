from django.db import models

class Artist(models.Model):
  artist_name = models.CharField(primary_key=True, max_length=255, null=False)
  
  def __str__(self):
    return self.artist_name

class Album(models.Model):
  album_id = models.CharField(primary_key=True, max_length=255, null=False)
  cover_url = models.CharField(max_length=255, null=False)
  genre_primary = models.CharField(max_length=255, null=False)
  genre_secondary = models.CharField(max_length=255, null=False)
  name = models.CharField(max_length=255, null=False)
  release_code = models.CharField(max_length=255, null=False)
  release_type = models.CharField(max_length=255, null=False, db_column="type")
  artist = models.ForeignKey(Artist, db_column="artist_name", on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Song(models.Model):
  track_id = models.IntegerField(primary_key=True, null=False)
  genre_primary = models.CharField(max_length=255, null=False)
  genre_secondary = models.CharField(max_length=255, null=False)
  song_id = models.CharField(max_length=255, null=False)
  url = models.CharField(max_length=255, null=False)
  title = models.CharField(max_length=255, null=False)
  track_number = models.IntegerField(null=False)
  album = models.ForeignKey(Album, db_column="album_id", on_delete=models.CASCADE, default="EMPTY")
  artist = models.ForeignKey(Artist, db_column="artist_name", on_delete=models.CASCADE, default="EMPTY")
  album_name = models.CharField(db_column="album", max_length=255, null=True)
  
  def __str__(self):
    return self.title