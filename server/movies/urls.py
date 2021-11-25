from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    path('allmovies/', views.allmovies), # 전체 영화 조회 + 페이지네이션
    path('allmovies/<int:movie_pk>/', views.movie_detail),
    path('allreviews/', views.allreviews),
    path('review/<int:movie_pk>/', views.review),
    path('review/change/<int:review_pk>/', views.review_delete_update),
    path('review/<int:review_pk>/comment/', views.comment),
    path('mylists/', views.get_my_list),
    path('mylists/<int:movie_pk>/', views.my_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('search/<str:keyword>/', views.search),
    path('db/genres/', views.get_genres_db),
    path('db/movies/', views.get_movies_db),
]
# 이런식으로 수정하시고 