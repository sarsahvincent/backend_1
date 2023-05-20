from django.urls import path
from . import views
from .views import RegisterView, LoginView

urlpatterns = [
    path('products/', views.get_products, name='products'),
    path('products/<str:pk>/', views.get_product, name='product'),
    path('user/login/', views.MyTokenObjectPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]
