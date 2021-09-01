from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import (
    CharField,
    IntegerField
)
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User


class RepositoryManager(models.Manager):
    def create_repository(self, name, user_id, repo_id):
        repository = self.create(name=name, user_id=user_id, repo_id=repo_id)
        # do something if needed
        return repository


class Repository(models.Model):
    name = CharField(max_length=255, verbose_name='Name')
    user_id = ForeignKey(User, on_delete=CASCADE)
    repo_id = IntegerField()

    objects = RepositoryManager()

    # repo = Repository.objects.create_repository(...)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'repo_id'], name='user_repo_id_constraint')
        ]

    def __str__(self):
        return self.name

