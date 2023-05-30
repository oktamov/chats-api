from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import User, Message


class UserRegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'photo', 'email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.get("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'photo', 'email', 'username']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user:
            attrs['user'] = user
            return attrs

        else:
            msg = 'avval royxatdan o\'t'
            raise serializers.ValidationError(msg, code='authorization')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'created_at']


class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']
