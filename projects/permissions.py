from rest_framework import permissions
from .models import Contributor


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée qui permet seulement aux auteurs d'un objet
    de le modifier ou le supprimer.
    """

    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissions d'écriture seulement pour l'auteur de l'objet
        return obj.author == request.user


class IsProjectContributor(permissions.BasePermission):
    """
    Permission qui vérifie que l'utilisateur est contributeur du projet
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Pour les vues de projets
        if hasattr(view, 'get_object'):
            try:
                project = view.get_object()
                return Contributor.objects.filter(
                    project=project,
                    user=request.user
                ).exists()
            except:
                return True  # Laisse passer pour les autres validations
        
        return True

    def has_object_permission(self, request, view, obj):
        # Pour les objets Project
        if hasattr(obj, 'contributors'):
            return Contributor.objects.filter(
                project=obj,
                user=request.user
            ).exists()
        
        # Pour les objets liés à un projet (Issue, Comment)
        if hasattr(obj, 'project'):
            return Contributor.objects.filter(
                project=obj.project,
                user=request.user
            ).exists()
        
        # Pour les objets Comment (liés via Issue)
        if hasattr(obj, 'issue'):
            return Contributor.objects.filter(
                project=obj.issue.project,
                user=request.user
            ).exists()
        
        return False


class IsProjectAuthorOrContributorReadOnly(permissions.BasePermission):
    """
    Permission qui permet aux auteurs de projet de faire toutes les opérations,
    et aux contributeurs de seulement lire
    """

    def has_object_permission(self, request, view, obj):
        # Vérifier que l'utilisateur est contributeur du projet
        is_contributor = Contributor.objects.filter(
            project=obj,
            user=request.user
        ).exists()
        
        if not is_contributor:
            return False

        # Si c'est une méthode de lecture, autoriser tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            return True

        # Pour les opérations de modification, vérifier que c'est l'auteur
        return obj.author == request.user


class CanManageContributors(permissions.BasePermission):
    """
    Permission pour gérer les contributeurs d'un projet.
    Seul l'auteur du projet peut ajouter/supprimer des contributeurs.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Pour les objets Contributor, vérifier que l'utilisateur est l'auteur du projet
        if hasattr(obj, 'project'):
            return obj.project.author == request.user
        return False
