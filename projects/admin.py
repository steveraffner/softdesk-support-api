from django.contrib import admin
from .models import Project, Contributor, Issue, Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Project
    """
    list_display = ('name', 'type', 'author', 'created_time')
    list_filter = ('type', 'created_time')
    search_fields = ('name', 'description', 'author__username')
    readonly_fields = ('created_time',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Contributor
    """
    list_display = ('user', 'project', 'created_time')
    list_filter = ('created_time',)
    search_fields = ('user__username', 'project__name')
    readonly_fields = ('created_time',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Issue
    """
    list_display = ('name', 'project', 'author', 'assignee', 'priority', 'tag', 'status', 'created_time')
    list_filter = ('priority', 'tag', 'status', 'created_time')
    search_fields = ('name', 'description', 'project__name', 'author__username')
    readonly_fields = ('created_time',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Comment
    """
    list_display = ('id', 'issue', 'author', 'created_time')
    list_filter = ('created_time',)
    search_fields = ('description', 'issue__name', 'author__username')
    readonly_fields = ('id', 'created_time')
