from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.db.models import Q
import re
from django.utils import timezone


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please enter an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("PM", 'Project Manager'),
        ("DPM", 'Digital Project Manager'),
        ("WD", 'Web Developer'),
        ("OM", 'Operations Manager'),
        ("AM", 'Account Manager'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=3)
    is_staff = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return re.split('\d*\W*@', self.email)[0]


class Project(models.Model):
    name = models.CharField(max_length=200)
    client = models.CharField(max_length=200, default='Internal')
    project_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, limit_choices_to=Q(role__contains="PM"))
    description = models.TextField(default="")
    started = models.DateTimeField(
        "start date", blank=True, default=timezone.now)
    completed = models.DateTimeField("completion date", blank=True, null=True)

    def __str__(self):
        return self.name


class TicketCategory(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Ticket Categories"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("Open", 'Open'),
        ("In Progress", 'In Progress'),
        ("Closed", 'Closed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        TicketCategory, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=15, default='Open')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
