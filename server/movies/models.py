from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Actor(models.Model):  # cast
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_path = models.TextField(null=True)

    def __str__(self):
        return f'{self.id}: {self.name}'


class Director(models.Model):  # crew
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    profile_path = models.TextField(null=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

# 장르
# class Genre(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return f'{self.id}: {self.name}'
class Genre(models.Model):
    tmdb_genre_id = models.IntegerField()
    name = models.CharField(max_length=50)

# 영화
class Movie(models.Model):
    # genres ManyToMany로 가져오기
    genres = models.ManyToManyField(Genre, related_name='movies')
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    adult = models.BooleanField()
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField(null=True)
    original_language = models.CharField(max_length=20)
    original_title = models.CharField(max_length=200)
    backdrop_path = models.TextField(null=True)
    poster_path = models.TextField(null=True)
    video = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}: {self.title}'

# 리뷰
class Review(models.Model): # review.user && review.movie // user.reviewing. // movie.reviewed.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewing')
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviewed')
    rank = models.IntegerField()
    title = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 댓글
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# 내 영화 리스트
class Mylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='list_users')
    title = models.CharField(max_length=100)
    poster_path = models.TextField()
