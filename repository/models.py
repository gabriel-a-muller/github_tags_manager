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
