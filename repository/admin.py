from django.contrib import admin
from repository.models import Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user_id', 'repo_id')
    list_display_links = ('id', 'name')

admin.site.register(Repository, RepositoryAdmin)