from statistics import mode
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.username


def post_user_create_signal(sender, instance, created, **kwargs):
    if created and not instance.is_agent and instance.is_organisor:
        Organization.objects.create(user=instance)

post_save.connect(post_user_create_signal, sender=User)