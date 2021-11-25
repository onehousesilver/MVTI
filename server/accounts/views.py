from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserProfileSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from movies.models import Movie, Review
from movies.serializers import ReviewSerializer, ReviewSerializerTest, ReviewedMovieSerializer

from accounts import serializers

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
	# 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
	# 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=request.data.get('username')).exists():
        return Response({'error': '일치하는 이메일이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=request.data.get('nickname')).exists():
        return Response({'error': '일치하는 닉네임이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)

	# 2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)
	# 3. validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #4. 비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다. (write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # image = request.data.get('image')
        if request.user.username != request.data.get('username') and User.objects.filter(username=request.data.get('username')).exists():
            return Response({'error': '일치하는 닉네임이 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserProfileSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        user_pk = request.user.pk
        request.user.delete()
        return Response({ 'delete': f'{user_pk}번 회원이 탈퇴했습니다.' }, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def reviewed_movie(request, user_pk):
    print(request)
    reviews = Review.objects.filter(user_id=user_pk).order_by('-pk')
    serializers = ReviewedMovieSerializer(reviews, many=True)
    return Response(serializers.data)
    """
    if request.method == 'GET':
        reviews = Review.objects.filter(movie_id=movie_pk).order_by('-pk')
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    """