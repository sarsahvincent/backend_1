from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers.serializers import ProductSerializer, UserSerializerToken
from .models import Product
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from base.serializers.serializers import UserSerializer, UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token


class MyTokenObjectPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenObjectPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerToken(self.user).data

        for key, value in serializer.items():
            data[key] = value

        return data


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        response = {
            'success': True,
            'message': 'User registered successfully',
            'data': user_data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        response = {
            'success': True,
            'message': 'User logged in successfully',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)

    product = None

    return Response(serializer.data)
