from django.views.generic.list import ListView

from .models import Profile


class UserListView(ListView):

    def get_queryset(self):
        return Profile.objects.all()
