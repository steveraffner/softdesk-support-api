import uuid
from django.db import models
from django.conf import settings


class Project(models.Model):
    """
    Modèle représentant un projet client
    """
    
    PROJECT_TYPES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]
    
    name = models.CharField(
        max_length=255,
        verbose_name="Nom du projet"
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True
    )
    type = models.CharField(
        max_length=10,
        choices=PROJECT_TYPES,
        verbose_name="Type de projet"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects',
        verbose_name="Auteur"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_time']
    
    def __str__(self):
        return self.name


class Contributor(models.Model):
    """
    Modèle de liaison entre User et Project (relation many-to-many)
    Un utilisateur peut contribuer à plusieurs projets
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributions',
        verbose_name="Utilisateur"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='contributors',
        verbose_name="Projet"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Contributeur"
        verbose_name_plural = "Contributeurs"
        unique_together = ('user', 'project')  # Un utilisateur ne peut contribuer qu'une fois au même projet
        ordering = ['-created_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.project.name}"


class Issue(models.Model):
    """
    Modèle représentant un problème/tâche dans un projet
    """
    
    PRIORITY_CHOICES = [
        ('LOW', 'Faible'),
        ('MEDIUM', 'Moyenne'),
        ('HIGH', 'Élevée'),
    ]
    
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Fonctionnalité'),
        ('TASK', 'Tâche'),
    ]
    
    STATUS_CHOICES = [
        ('TO_DO', 'À faire'),
        ('IN_PROGRESS', 'En cours'),
        ('FINISHED', 'Terminé'),
    ]
    
    name = models.CharField(
        max_length=255,
        verbose_name="Nom de l'issue"
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues',
        verbose_name="Projet"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_issues',
        verbose_name="Auteur"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues',
        verbose_name="Assigné à"
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM',
        verbose_name="Priorité"
    )
    tag = models.CharField(
        max_length=10,
        choices=TAG_CHOICES,
        verbose_name="Étiquette"
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='TO_DO',
        verbose_name="Statut"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Issue"
        verbose_name_plural = "Issues"
        ordering = ['-created_time']
    
    def __str__(self):
        return f"{self.name} - {self.project.name}"


class Comment(models.Model):
    """
    Modèle représentant un commentaire sur une issue
    """
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Identifiant unique"
    )
    description = models.TextField(
        verbose_name="Commentaire"
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Issue"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_comments',
        verbose_name="Auteur"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_time']
    
    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.issue.name}"
