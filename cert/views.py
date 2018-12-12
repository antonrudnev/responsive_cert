from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .models import Profile


class UserListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Profile.objects.all()
