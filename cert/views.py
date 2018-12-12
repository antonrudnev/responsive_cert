from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView

from .models import Profile, Credential


class UserListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Profile.objects.all()


class CertificatesListView(ListView):
    def get_queryset(self):
        return Credential.objects.all()
