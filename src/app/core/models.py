from typing import TYPE_CHECKING
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.fields import proxy
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    # required
    username = models.CharField(max_length=30, unique=True, blank=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    second_name = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=30, null=True, blank=True)

    # optional
    favourites = models.ManyToManyField('core.Collector', blank=True)
    
    @property
    def visit_count(self):
        len(Visit.objects.filter(user=self))

    # system
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser


class Contact(models.Model):
    phone_number = models.CharField(max_length=12)
    email = models.EmailField()


class Collector(models.Model):
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)    
    name = models.CharField(max_length=200)
    TYPE_CHOICES = [
        ('general', 'Общего назначения'),
        ('plastic', 'Для пластика'),
        ('glass', 'Для стекла'),
        ('paper', 'Для бумаги'),
        ('batteries', 'Для батареек')
    ]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, blank=True, null=True)
    photo = models.ImageField()
    description = models.TextField()
    collector_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def visited_count(self):
        return len(Visit.objects.filter(visit_collector=self))


class Visit(models.Model):
    visit_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    visit_collector = models.ForeignKey(Collector, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)


class VisitAchievement(models.Model):
    header = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(max_length=150)
    image = models.ImageField()
    visit_amount = models.IntegerField()

