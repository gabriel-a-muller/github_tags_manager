from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import (
    CharField,
    IntegerField,
    TextField,
    DateField,
    URLField
)
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

from taggit.managers import TaggableManager


class RepositoryManager(models.Manager):
    def create_repository(self, name, user, repo_id, description, created_date, url):
        repository = self.create(
            name=name,
            user=user,
            repo_id=repo_id,
            description=description,
            created_at_date=created_date,
            url=url
            )
        return repository

    def get_custom_queryset(self, **kwargs):
        queryset = self.all().order_by('-created_at_date')

        # Mandatory filter
        user = kwargs.get('user')
        # Optional filters
        name = kwargs.get('name', None)
        repo_id = kwargs.get('repo_id', None)
        description = kwargs.get('description', None)
        created_at_date = kwargs.get('created_at_date', None)
        url = kwargs.get('url', None)
        tags = kwargs.get('tags', None)

        # Settings filters
        queryset = queryset.filter(user=user)

        if name:
            queryset = queryset.filter(name=name)
        if repo_id:
            queryset = queryset.filter(repo_id=repo_id)
        if description:
            queryset = queryset.filter(description=description)
        if created_at_date:
            queryset = queryset.filter(created_at_date=created_at_date)
        if url:
            queryset = queryset.filter(url=url)
        if tags:
            queryset = queryset.filter(tags=tags)

        return queryset




class Repository(models.Model):
    name = CharField(max_length=255, verbose_name='Name')
    user = ForeignKey(User, on_delete=CASCADE)
    repo_id = IntegerField()
    description = TextField(null=True)
    created_at_date = DateField()
    tags = TaggableManager()
    url = URLField(max_length=255)

    objects = RepositoryManager()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'repo_id'], name='user_repo_id_constraint')
        ]

    def __str__(self):
        return self.name
