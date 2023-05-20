from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers.serializers import ProductSerializer, UserSerializerToken
from .models import Product, User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from base.serializers.serializers import UserSerializer, UserSerializer, UserSerializerWithToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    # this add the selected fields to the refresh and access token
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for key, value in serializer.items():
            data[key] = value
        # data['username'] = self.user.username
        # data['email'] = self.user.email

        return data


# this will require user to decode the token in other to get the added information
"""     @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token """


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
@permission_classes([IsAdminUser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uer_profile(request):
    """ 
    because of the token base authentication, the user will not be the login user 
    it will get the login user token from the decorator
    """

    user = request.user
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)


@api_view(['GET'])
def get_product(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)

    product = None

    return Response(serializer.data)
