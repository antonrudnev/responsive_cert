from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=256, null=False, blank=False)
    organization = models.CharField(max_length=256, null=True, blank=True)
    public_key = models.CharField(max_length=256, null=True, blank=True)
    private_key = models.CharField(max_length=256, null=True, blank=True)
    cert_template = models.TextField(null=True, blank=True)


class Credential(models.Model):
    issuer = models.ForeignKey(Profile, related_name="issuers", on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, related_name="owners", on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=False, blank=False)
    cert_content = models.TextField()
    transaction_id = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30)
