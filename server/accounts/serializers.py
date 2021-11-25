from rest_framework import serializers
# from movies.serializers import ReviewSerializer, MovieSerializer
from django.contrib.auth import get_user_model


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'nickname', 'mbti',)

class UserProfileSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'mbti',)