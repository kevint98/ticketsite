from django.contrib import admin
from .models import Role, User, Project, IssueCategory, Issue


# Register your models here.

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Project)
admin.site.register(IssueCategory)
admin.site.register(Issue)
