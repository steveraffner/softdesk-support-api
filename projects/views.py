from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer, ContributorSerializer, 
    IssueSerializer, CommentSerializer
)
from .permissions import (
    IsAuthorOrReadOnly, IsProjectContributor,
    IsProjectAuthorOrContributorReadOnly, CanManageContributors
)


@extend_schema_view(
    list=extend_schema(
        summary="Liste des projets",
        description="Récupérer la liste des projets auxquels l'utilisateur contribue",
        tags=["Projets"]
    ),
    create=extend_schema(
        summary="Créer un projet",
        description="Créer un nouveau projet (l'auteur devient automatiquement contributeur)",
        tags=["Projets"]
    ),
    retrieve=extend_schema(
        summary="Détails d'un projet",
        description="Récupérer les détails d'un projet spécifique",
        tags=["Projets"]
    ),
    update=extend_schema(
        summary="Modifier un projet",
        description="Modifier un projet (seul l'auteur peut modifier)",
        tags=["Projets"]
    ),
    destroy=extend_schema(
        summary="Supprimer un projet",
        description="Supprimer un projet (seul l'auteur peut supprimer)",
        tags=["Projets"]
    )
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthorOrContributorReadOnly]

    def get_queryset(self):
        """
        Retourne seulement les projets auxquels l'utilisateur contribue
        """
        user = self.request.user
        contributed_projects = Contributor.objects.filter(user=user).values_list('project', flat=True)
        return Project.objects.filter(id__in=contributed_projects)

    @extend_schema(
        summary="Liste des contributeurs",
        description="Récupérer la liste des contributeurs d'un projet",
        tags=["Projets"]
    )
    @action(detail=True, methods=['get'])
    def contributors(self, request, pk=None):
        """
        Action personnalisée pour lister les contributeurs d'un projet
        """
        project = self.get_object()
        contributors = Contributor.objects.filter(project=project)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Ajouter un contributeur",
        description="Ajouter un contributeur au projet (seul l'auteur peut ajouter)",
        tags=["Projets"]
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, CanManageContributors])
    def add_contributor(self, request, pk=None):
        """
        Action personnalisée pour ajouter un contributeur à un projet
        """
        project = self.get_object()
        serializer = ContributorSerializer(
            data=request.data,
            context={'request': request, 'project': project}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Supprimer un contributeur",
        description="Supprimer un contributeur du projet (seul l'auteur peut supprimer)",
        tags=["Projets"]
    )
    @action(detail=True, methods=['delete'], url_path='contributors/(?P<contributor_id>[^/.]+)')
    def remove_contributor(self, request, pk=None, contributor_id=None):
        """
        Action personnalisée pour supprimer un contributeur d'un projet
        """
        project = self.get_object()
        contributor = get_object_or_404(Contributor, id=contributor_id, project=project)
        
        # Vérifier que ce n'est pas l'auteur du projet
        if contributor.user == project.author:
            return Response({
                'error': "L'auteur du projet ne peut pas être supprimé des contributeurs."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        summary="Liste des issues",
        description="Récupérer la liste des issues d'un projet",
        tags=["Issues"]
    ),
    create=extend_schema(
        summary="Créer une issue",
        description="Créer une nouvelle issue dans un projet",
        tags=["Issues"]
    ),
    retrieve=extend_schema(
        summary="Détails d'une issue",
        description="Récupérer les détails d'une issue spécifique",
        tags=["Issues"]
    ),
    update=extend_schema(
        summary="Modifier une issue",
        description="Modifier une issue (seul l'auteur peut modifier)",
        tags=["Issues"]
    ),
    destroy=extend_schema(
        summary="Supprimer une issue",
        description="Supprimer une issue (seul l'auteur peut supprimer)",
        tags=["Issues"]
    )
)
class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les issues d'un projet
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retourne les issues du projet spécifié
        """
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id)

    def get_serializer_context(self):
        """
        Ajoute le projet au contexte du serializer
        """
        context = super().get_serializer_context()
        project_id = self.kwargs.get('project_pk')
        if project_id:
            context['project'] = get_object_or_404(Project, id=project_id)
        return context


@extend_schema_view(
    list=extend_schema(
        summary="Liste des commentaires",
        description="Récupérer la liste des commentaires d'une issue",
        tags=["Commentaires"]
    ),
    create=extend_schema(
        summary="Créer un commentaire",
        description="Créer un nouveau commentaire sur une issue",
        tags=["Commentaires"]
    ),
    retrieve=extend_schema(
        summary="Détails d'un commentaire",
        description="Récupérer les détails d'un commentaire spécifique",
        tags=["Commentaires"]
    ),
    update=extend_schema(
        summary="Modifier un commentaire",
        description="Modifier un commentaire (seul l'auteur peut modifier)",
        tags=["Commentaires"]
    ),
    destroy=extend_schema(
        summary="Supprimer un commentaire",
        description="Supprimer un commentaire (seul l'auteur peut supprimer)",
        tags=["Commentaires"]
    )
)
class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires d'une issue
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Retourne les commentaires de l'issue spécifiée
        """
        issue_id = self.kwargs.get('issue_pk')
        return Comment.objects.filter(issue_id=issue_id)

    def get_serializer_context(self):
        """
        Ajoute l'issue au contexte du serializer
        """
        context = super().get_serializer_context()
        issue_id = self.kwargs.get('issue_pk')
        if issue_id:
            context['issue'] = get_object_or_404(Issue, id=issue_id)
        return context
