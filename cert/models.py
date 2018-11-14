from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as SystemUser


# user model
class User(models.Model):
    user = models.OneToOneField(SystemUser, primary_key = True, on_delete = models.CASCADE)
    description = models.TextField()
    public_key = models.CharField(max_length = 256, null = True)
    private_key = models.CharField(max_length = 256, null = True)
    cert_template = models.TextField(null = True)
  
    def _str_(self):
        return "%s" %(self.description)


# cert_credential model
class Credential(models.Model):
    issuer = models.ForeignKey(User, related_name = "issuers", on_delete = models.CASCADE)
    owner = models.ForeignKey(User, related_name = "owners", on_delete = models.CASCADE)
    cert_content = models.TextField()
    transaction_id = models.TextField()
    created_on = models.DateTimeField(default = timezone.now)
    status = models.CharField(max_length = 30)
  
    def _str_(self):
        return "%s" %(self.cert_content)
