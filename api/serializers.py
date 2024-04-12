from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Club


class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'
        

class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
