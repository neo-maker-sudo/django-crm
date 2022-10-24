from django.db import models
from agents.models import Agent
from base.models import Organization
from category.models import Category


class LeadManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, related_name="leads", on_delete=models.SET_NULL, null=True, blank=True)

    objects = LeadManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"