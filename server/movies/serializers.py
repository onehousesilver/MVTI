from rest_framework import serializers
from accounts.serializers import UserProfileSerializer, UserSerializer
from .models import Genre, Movie, Actor, Director, Comment, Mylist, Review


########################## 배우 ###########################
class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

########################## 감독 ###########################
class DirectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Director
        fields = '__all__'

########################## 장르 ###########################
class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

########################## 리뷰, 리뷰목록 ###########################
class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'review', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('review',)

class ReviewSerializer(serializers.ModelSerializer):
    movies = serializers.IntegerField(source='movie.count', read_only=True)
    user = UserProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'user', 'movie', 'rank', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comments_count', 'movies')
        read_only_fields = ('movie',)

class ReviewSerializerTest(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'rank',)

########################## 영화, 영화목록 ###########################
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='reviews.count', read_only=True)

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    genre_ids = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        # fields = ('id', 'title', 'adult', 'release_date', 'popularity', 'vote_count', 'vote_average', 'overview')


# 프로필의 리뷰한 영화
class ReviewedMovieSerializer(serializers.ModelSerializer):
    # movie = MovieSerializer(many=True, read_only=True)
    poster = serializers.CharField(source='movie.poster_path', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'content', 'rank', 'movie', 'poster', 'movie_title', 'updated_at', )
        # fields = '__all__'


# 리스트추가
class MylistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_mbti = serializers.CharField(source='user.mbti', read_only=True)

    class Meta:
        model = Mylist
        fields = ('id', 'user', 'movie', 'title', 'poster_path', 'user_mbti', )
        read_only_fields = ('user', 'movie', 'title', 'poster_path', 'user_mbti', )