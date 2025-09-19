from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from datetime import date


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec des champs RGPD pour le consentement
    et la vérification d'âge (minimum 15 ans).
    """
    
    # Champs supplémentaires pour le RGPD
    birth_date = models.DateField(
        verbose_name="Date de naissance",
        help_text="Nécessaire pour vérifier l'âge minimum (15 ans)"
    )
    can_be_contacted = models.BooleanField(
        default=False,
        verbose_name="Peut être contacté",
        help_text="L'utilisateur consent à être contacté"
    )
    can_data_be_shared = models.BooleanField(
        default=False,
        verbose_name="Peut partager les données",
        help_text="L'utilisateur consent au partage de ses données"
    )
    
    # Métadonnées
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_time']
    
    def __str__(self):
        return self.username
    
    @property
    def age(self):
        """Calcule l'âge de l'utilisateur"""
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    def clean(self):
        """Validation personnalisée pour s'assurer que l'utilisateur a au moins 15 ans"""
        from django.core.exceptions import ValidationError
        if self.birth_date and self.age < 15:
            raise ValidationError(
                "L'utilisateur doit avoir au moins 15 ans pour s'inscrire selon les règles RGPD."
            )
    
    def save(self, *args, **kwargs):
        """Appelle clean() avant de sauvegarder"""
        self.clean()
        super().save(*args, **kwargs)
