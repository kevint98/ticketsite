from django.contrib import admin
from .models import User, Project, TicketCategory, Ticket


# Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(TicketCategory)
admin.site.register(Ticket)
