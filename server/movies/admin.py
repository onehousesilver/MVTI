from django.contrib import admin
from .models import Movie, Review, Genre, Comment
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'review' , 'content' , 'created_at', 'updated_at']
    
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'original_title', 'release_date', 'popularity', 'overview', 'poster_path', 'backdrop_path']

class GenreAdmin(admin.ModelAdmin):
    list_display = ['tmdb_genre_id', 'name']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie', 'title', 'content', 'created_at', 'updated_at']


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)