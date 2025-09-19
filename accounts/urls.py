from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView, UserProfileView, 
    delete_user_account, CustomTokenObtainPairView
)

app_name = 'accounts'

urlpatterns = [
    # Authentification
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Profil utilisateur (RGPD)
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('delete-account/', delete_user_account, name='delete_account'),
]
