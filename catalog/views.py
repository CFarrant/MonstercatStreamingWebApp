from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.template import loader
from catalog.models import Album, Song
from random import randint
from .forms import Registration, Login
import datetime

# General views:
def index(request):
  try:
    temp = request.session['is_logged_in']
  except KeyError:
    request.session['is_logged_in'] = False
  try:
    temp = request.session['is_admin']
  except KeyError:
    request.session['is_admin'] = False
  context = {
    'logged_in': request.session['is_logged_in'],
    'admin': request.session['is_admin'],
  }
  return render(request, 'catalog\index.html', context)

def random(request):
  randomAlbum = randint(0, len(Album.objects.all())-1)
  album = Album.objects.all()[randomAlbum]
  albumSongs = Song.objects.filter(album_id=album.album_id)
  randomSong = randint(0, len(albumSongs)-1)
  song = albumSongs[randomSong]
  artist = song.artist
  context = {
    'album_cover_url': album.cover_url,
    'artist_name': artist.artist_name,
    'song_title': song.title,
    'genre_primary': song.genre_primary,
    'genre_secondary': song.genre_secondary,
    'song_url': song.url,
    'logged_in': request.session['is_logged_in'],
    'admin': request.session['is_admin'],
  }
  return render(request, 'catalog\\random.html', context)

#If user is logged out:
def login(request):
  form = Login()
  if request.method == "GET":
    return render(request, 'catalog\\login.html', {'form': form})
  elif request.method == "POST":
    form = Login(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      user = authenticate(username=email, password=password)
      if user is not None:
        request.session['is_logged_in'] = True
        if user in User.objects.filter(is_superuser=True):
          request.session['is_admin'] = True
        return redirect("/")
      else:
        return redirect("/login/")
    else:
      return redirect("/login/")
  else:
    return redirect("/")

def register(request):
  form = Registration()
  if request.method == "GET":
    return render(request, 'catalog\\register.html', {'form': form})
  elif request.method == "POST":
    form = Registration(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      password = form.cleaned_data['password']
      password_verify = form.cleaned_data['password_verify']
      if password == password_verify:
        user = User.objects.create_user(email, email, password)
        print("User:",email,email,password)
        return redirect("/login/")
      else:
        return redirect("/register/")
    else:
      return redirect("/register/")
  else:
    return redirect("/")

#If user is logged in:
def catalog(request):
  if request.session["is_logged_in"] is True:
    albums = Album.objects.all()
    context = {
      'albums': albums,
      'logged_in': request.session['is_logged_in'],
      'admin': request.session['is_admin'],
    }
    return render(request, 'catalog\catalog.html', context)
  else:
    return redirect("/login/")

def album(request):
  if request.session["is_logged_in"] is True:
    if request.method == "GET":
      id = request.GET.get('id')
      if not id:
        return redirect("/catalog/")
      else:
        album = Album.objects.get(album_id=id)
        songs = Song.objects.filter(album_id=id)
        context = {
          "album": album,
          "songs": songs,
          "logged_in": request.session['is_logged_in'],
          'admin': request.session['is_admin'],
        }
        return render(request, 'catalog\\album.html', context)
    else:
      return redirect("/")
  else:
    return redirect("/login/")

def song(request):
  if request.session["is_logged_in"] is True:
    if request.method == "GET":
      id = request.GET.get('id')
      if not id:
        return redirect("/catalog/")
      else:
        song = Song.objects.get(track_id=id)
        context = {
          'album_cover_url': song.album.cover_url,
          'artist_name': song.artist.artist_name,
          'song_title': song.title,
          'genre_primary': song.genre_primary,
          'genre_secondary': song.genre_secondary,
          'song_url': song.url,
          'logged_in': request.session['is_logged_in'],
          'admin': request.session['is_admin'],
        }
        return render(request, 'catalog\\song.html', context)
    else:
      return redirect("/")
  else:
    return redirect("/login/")

def logout(request):
  request.session['is_logged_in'] = False
  request.session['is_admin'] = False
  return redirect("/")