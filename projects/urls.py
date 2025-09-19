from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet, CommentViewSet

app_name = 'projects'

# Router principal pour les projets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

# Pour le moment, on va créer des URLs simples pour les issues et commentaires
# Plus tard on pourra les imbriquer avec rest_framework_nested

urlpatterns = [
    path('', include(router.urls)),
    # URLs temporaires pour les issues et commentaires
    path('projects/<int:project_pk>/issues/', IssueViewSet.as_view({'get': 'list', 'post': 'create'}), name='project-issues-list'),
    path('projects/<int:project_pk>/issues/<int:pk>/', IssueViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='project-issues-detail'),
    path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='issue-comments-list'),
    path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<uuid:pk>/', CommentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='issue-comments-detail'),
]
