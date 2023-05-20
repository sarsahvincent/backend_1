from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User
from base.models import Product


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', '_id', 'isAdmin']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_user(self, obt):
        name = obt.first_name

        if name == "":
            name = obt.email
        return name


class UserSerializerToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password',
                  'name', '_id', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return token


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
