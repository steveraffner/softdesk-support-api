from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from accounts.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour les projets
    """
    author = UserSerializer(read_only=True)
    contributors_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'type', 'author', 
            'contributors_count', 'created_time'
        ]
        read_only_fields = ['id', 'author', 'created_time']

    def get_contributors_count(self, obj):
        """Retourne le nombre de contributeurs du projet"""
        return obj.contributors.count()

    def create(self, validated_data):
        """Crée un projet et ajoute automatiquement l'auteur comme contributeur"""
        user = self.context['request'].user
        project = Project.objects.create(author=user, **validated_data)
        # L'auteur devient automatiquement contributeur
        Contributor.objects.create(user=user, project=project)
        return project


class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour les contributeurs
    """
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'user_id', 'project', 'created_time']
        read_only_fields = ['id', 'project', 'created_time']

    def validate_user_id(self, value):
        """Valide que l'utilisateur existe"""
        from accounts.models import User
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Cet utilisateur n'existe pas.")
        return value

    def validate(self, attrs):
        """Valide qu'un utilisateur n'est pas déjà contributeur du projet"""
        project = self.context.get('project')
        user_id = attrs.get('user_id')
        
        if Contributor.objects.filter(project=project, user_id=user_id).exists():
            raise serializers.ValidationError(
                "Cet utilisateur est déjà contributeur de ce projet."
            )
        return attrs

    def create(self, validated_data):
        """Crée un nouveau contributeur"""
        project = self.context['project']
        user_id = validated_data.pop('user_id')
        from accounts.models import User
        user = User.objects.get(id=user_id)
        return Contributor.objects.create(user=user, project=project)


class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour les issues
    """
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id', 'name', 'description', 'project', 'project_name',
            'author', 'assignee', 'assignee_id', 'priority', 'tag', 
            'status', 'comments_count', 'created_time'
        ]
        read_only_fields = ['id', 'project', 'author', 'created_time']

    def get_comments_count(self, obj):
        """Retourne le nombre de commentaires de l'issue"""
        return obj.comments.count()

    def validate_assignee_id(self, value):
        """Valide que l'assigné est un contributeur du projet"""
        if value is not None:
            project = self.context.get('project')
            if not Contributor.objects.filter(project=project, user_id=value).exists():
                raise serializers.ValidationError(
                    "L'utilisateur assigné doit être un contributeur du projet."
                )
        return value

    def create(self, validated_data):
        """Crée une nouvelle issue"""
        user = self.context['request'].user
        project = self.context['project']
        assignee_id = validated_data.pop('assignee_id', None)
        
        issue = Issue.objects.create(
            author=user,
            project=project,
            assignee_id=assignee_id,
            **validated_data
        )
        return issue


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer pour les commentaires
    """
    author = UserSerializer(read_only=True)
    issue_name = serializers.CharField(source='issue.name', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'description', 'issue', 'issue_name',
            'author', 'created_time'
        ]
        read_only_fields = ['id', 'issue', 'author', 'created_time']

    def create(self, validated_data):
        """Crée un nouveau commentaire"""
        user = self.context['request'].user
        issue = self.context['issue']
        return Comment.objects.create(
            author=user,
            issue=issue,
            **validated_data
        )
