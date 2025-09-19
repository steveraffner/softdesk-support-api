from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import User
from .serializers import UserRegistrationSerializer, UserSerializer, UserDeleteSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Inscription d'un nouvel utilisateur",
        description="Créer un nouveau compte utilisateur avec validation RGPD (âge minimum 15 ans)",
        tags=["Authentification"]
    )
)
class UserRegistrationView(generics.CreateAPIView):
    """
    Vue pour l'inscription des nouveaux utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        summary="Profil utilisateur",
        description="Récupérer les informations du profil utilisateur connecté",
        tags=["Utilisateurs"]
    ),
    put=extend_schema(
        summary="Modifier le profil",
        description="Modifier les informations du profil utilisateur (droit à la rectification RGPD)",
        tags=["Utilisateurs"]
    ),
    patch=extend_schema(
        summary="Modification partielle du profil",
        description="Modification partielle des informations du profil utilisateur",
        tags=["Utilisateurs"]
    )
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Vue pour consulter et modifier le profil utilisateur
    Implémente le droit à l'accès et à la rectification RGPD
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    summary="Suppression du compte utilisateur",
    description="Supprimer définitivement le compte utilisateur et toutes ses données (droit à l'oubli RGPD)",
    tags=["Utilisateurs"]
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_account(request):
    """
    Vue pour supprimer le compte utilisateur
    Implémente le droit à l'oubli RGPD
    """
    serializer = UserDeleteSerializer(data=request.data)
    if serializer.is_valid():
        # Supprimer l'utilisateur et toutes ses données associées
        user = request.user
        username = user.username
        user.delete()
        
        return Response({
            'message': f'Le compte {username} et toutes ses données ont été supprimés définitivement.'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour l'authentification JWT
    """
    
    @extend_schema(
        summary="Connexion utilisateur",
        description="Authentifier un utilisateur et obtenir des tokens JWT",
        tags=["Authentification"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
