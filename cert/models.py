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

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}' \
            if self.user.first_name or self.user.last_name else self.user.username

    class Meta:
        permissions = (
            ('view_issuer_profiles', 'Can see users who issue credentials'),
            ('view_owner_profiles', 'Can see users who own credentials'),
        )


class Credential(models.Model):
    issuer = models.ForeignKey(Profile, related_name='issued', on_delete=models.CASCADE, null=False, blank=False)
    owner = models.ForeignKey(Profile, related_name='owned', on_delete=models.CASCADE, null=False, blank=False)
    title = models.CharField(max_length=256, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    transaction_id = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now, null=False, blank=False)
    status = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return f'{self.title} ({self.owner})'

    class Meta:
        permissions = (
            ('view_all_credentials', 'Can see all credentials associated with the user'),
            ('issue_credentials', 'Can issue credentials to other users'),
            ('own_credentials', 'Can own credentials issued by other users'),
            ('verify_credentials', 'Can verify credentials'),
        )
