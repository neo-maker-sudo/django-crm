from django.db import models
from base.models import Organization


class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name