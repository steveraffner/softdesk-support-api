from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from datetime import date
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription des utilisateurs avec validation RGPD
    """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'birth_date',
            'can_be_contacted', 'can_data_be_shared'
        ]

    def validate_birth_date(self, value):
        """Valide que l'utilisateur a au moins 15 ans (RGPD)"""
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 15:
                raise serializers.ValidationError(
                    "Vous devez avoir au moins 15 ans pour créer un compte selon les règles RGPD."
                )
        return value

    def validate(self, attrs):
        """Validation globale incluant la confirmation du mot de passe"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Les mots de passe ne correspondent pas."
            })
        return attrs

    def create(self, validated_data):
        """Crée un nouvel utilisateur"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour la lecture et mise à jour des utilisateurs
    """
    age = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'birth_date', 'age', 'can_be_contacted', 'can_data_be_shared',
            'date_joined', 'created_time'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'created_time']

    def validate_birth_date(self, value):
        """Valide que l'utilisateur a au moins 15 ans (RGPD) même lors de la mise à jour"""
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age < 15:
                raise serializers.ValidationError(
                    "Vous devez avoir au moins 15 ans selon les règles RGPD."
                )
        return value


class UserDeleteSerializer(serializers.Serializer):
    """
    Serializer pour la suppression d'un utilisateur (Droit à l'oubli RGPD)
    """
    confirm_deletion = serializers.BooleanField(
        required=True,
        help_text="Confirmer la suppression définitive de toutes vos données personnelles"
    )

    def validate_confirm_deletion(self, value):
        if not value:
            raise serializers.ValidationError(
                "Vous devez confirmer la suppression pour procéder."
            )
        return value
