from django.core import paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import serializers

from .models import Movie, Genre, Review, Comment, Mylist
from .serializers import CommentSerializer, MovieSerializer, MovieListSerializer, ReviewSerializer, ReviewSerializerTest, MylistSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.core.paginator import Paginator
from django.http import HttpResponse

# 모든 영화
@api_view(['GET'])
@permission_classes([AllowAny])
def allmovies(request):
    movies = Movie.objects.order_by('-release_date')
    # movies = Movie.objects.all()
    paginator = Paginator(movies, 24)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     data = serializers.serialize('json', page_obj)
    #     return HttpResponse(data, content_type='application/json')
    # else:
    serializer = MovieSerializer(page_obj, many=True)
    return Response(serializer.data)

# 모든 리뷰
@api_view(['GET'])
@permission_classes([AllowAny])
def allreviews(request):
    reviews = Review.objects.order_by('-pk')
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

# 영화 디테일을 위한 영화 정보
@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)





# 리뷰 조회/생성
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':
        reviews = Review.objects.filter(movie_id=movie_pk).order_by('-pk')
        serializer = ReviewSerializer(reviews, many=True)
        paginator = Paginator(reviews, 10)

        # page_number = request.print("리뷰겟잘되냐?")GET.get('page_num')
        # reviews = paginator.get_page(page_number)
        # serializer = ReviewSerializer(reviews, many=True)
        # data = serializer.data
        # data.append({'possible_page': paginator.num_pages})
        # return Response(data)
        return Response(serializer.data)
    elif request.method == 'POST':
        # if Review.objects.filter(movie_id=movie_pk).exists():
        serializer = ReviewSerializerTest(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user.pk, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 리뷰 수정/삭제
@api_view(['DELETE', 'PUT'])
def review_delete_update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'DELETE':
            review.delete()
            data = {
                'delete' : f'{review_pk}번 리뷰가 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT':
            serializer = ReviewSerializer(review, data=request.data)
            print(request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

# 댓글 조회/생성
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':
        comments = Comment.objects.filter(review_id=review_pk).all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user_id=request.user.pk, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 삭제, 수정
@api_view(['DELETE'])
# @authentication_classes([JSONWebTokenAuthentication])
# @permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        if request.method == 'DELETE':
            comment.delete()
            data = {
                'delete' : f'{comment_pk}번 댓글이 삭제되었습니다.'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)
    return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


# 검색
@api_view(['GET'])
@permission_classes([AllowAny])
def search(request, keyword):
    movie = Movie.objects.filter(title__icontains=keyword).order_by('-release_date')
    if len(movie) > 0:
        serializer = MovieListSerializer(movie, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)        
    else:
        return Response({f'NO_CONTENT' : '${keyword}와 일치하는 영화가 없습니다.' }, status=status.HTTP_204_NO_CONTENT)


# 리스트 조회
@api_view(['GET'])
def get_my_list(request):
    lists = Mylist.objects.all()
    # lists = Mylist.objects.filter(user_id=request.data.get('user_id'))
    # paginator = Paginator(photo_tickets, 12)
    # page_num = request.GET.get('page_num')
    # photo_tickets = paginator.get_page(page_num)
    serializer = MylistSerializer(lists, many=True)
    data = serializer.data
    # data.append({'possible_page': paginator.num_pages})
    return Response(data)


# 리스트 생성, 삭제
@api_view(['GET', 'POST', 'DELETE'])
def my_list(request, movie_pk):
    if request.method == 'GET':
        lists = Mylist.objects.filter(user_id=movie_pk)
        serializer = MylistSerializer(lists, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie, poster_path=movie.poster_path, title=movie.title)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        list = Mylist.objects.filter(user__pk=request.user.pk, movie__pk=movie_pk).all()
        list.delete()
        data = {
            'delete' : '리스트에서 영화가 삭제되었습니다.'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)




# DB 구축용 ##########################################################################################
# 장르 DB에 넣어주기
@api_view(['POST'])
@permission_classes([AllowAny])
def get_genres_db(request):
    # if request.data.get('nickname') == 'admin':
    API_KEY = 'd398b98375f1cf45b81c4980e8e1c362'
    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&region=KR&language=ko'
    req = requests.get(url).json()
    Genre.objects.bulk_create(
        [Genre(
            tmdb_genre_id = data.get('id'),
            name = data.get('name'),
            ) for data in req.get('genres')]
    )
    return Response({ 'db': '가져왔습니다.' })
    # return Response({ 'Unauthorized': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)



# 영화 DB에 넣어주기
@api_view(['POST'])
@permission_classes([AllowAny])
def get_movies_db(request):
    # if request.data.get('username') == 'admin':
    API_KEY = 'd398b98375f1cf45b81c4980e8e1c362'
    for page in range(1, 30):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}&region=KR&language=ko'
        req = requests.get(url).json()
        for data in req.get('results'):
            if Movie.objects.filter(title=data.get('title')).exists():
                movie = Movie.objects.get(title=data.get('title'))
                movie.popularity = data.get('popularity')
                movie.vote_average = data.get('vote_average')
                movie.vote_count = data.get('vote_count')
                movie.save()
            else:
                movie = Movie.objects.create(
                    id = data.get('id'),
                    adult = data.get('adult'),
                    title = data.get('title'),
                    original_title = data.get('original_title'), 
                    release_date = data.get('release_date'),
                    popularity = data.get('popularity'),
                    vote_average = float(data.get('vote_average')),
                    vote_count = data.get('vote_count'),
                    overview = data.get('overview'),
                    poster_path = 'https://image.tmdb.org/t/p/w500' + data.get('poster_path'),
                    backdrop_path = 'https://image.tmdb.org/t/p/w500' + data.get('backdrop_path') if data.get('backdrop_path') else data.get('poster_path'),
                )
                for genre_id in data.get('genre_ids'):
                    genre = Genre.objects.get(tmdb_genre_id=genre_id)
                    genre.movies.add(movie)
    return Response({ 'db': 'DB에 가져온 영화를 저장했습니다.' })
    # return Response({ 'Unauthorized': '관리자 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)