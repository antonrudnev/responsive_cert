from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Profile, Credential


class UserListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Profile.objects.all()


class UserDetailView(DetailView):

    model = Profile

    # def get_queryset(self):
    #     return Profile.objects.filter(user_id=self.kwargs['user_id']).first()
    # def get_context_data(self, **kwargs):
    #     context = super(UserDetailView, self).get_context_data(**kwargs)
    #     context['profile'] = Profile.objects.filter(user__id=self.kwargs['user_id']).first()
    #     return context


class CredentialListView(ListView):

    def get_queryset(self):
        return Credential.objects.filter(owner__user_id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super(CredentialListView, self).get_context_data(**kwargs)
        context.update({'profile': Profile.objects.filter(user__id=self.kwargs['user_id']).first()})
        return context
