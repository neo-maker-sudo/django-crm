from django.db import models
from base.models import User, Organization


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username
