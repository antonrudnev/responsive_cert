from django.views.generic.list import ListView
from django.views.generic.detail import  DetailView
from django.views import View

from .models import Profile, Credential


class UserListView(ListView):
    template_name = 'profile_list.html'
    def get_queryset(self):
        return Profile.objects.all()


class CertificatesListView(ListView):
    #template_name = 'credentials_list.html'
    def get_queryset(self):
        return Credential.objects.all()
