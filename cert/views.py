from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Profile, Credential

import json


class UserListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Profile.objects.all()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = Profile


class CredentialListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        return Credential.objects.filter(owner__user_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(CredentialListView, self).get_context_data(**kwargs)
        context.update({'profile': Profile.objects.filter(user__id=self.kwargs['pk']).first()})
        context.update({'issued_credentials': Credential.objects.filter(issuer__user_id=self.kwargs['pk'])})
        return context


class CredentialDetailView(LoginRequiredMixin, DetailView):
    model = Credential

    def get_context_data(self, **kwargs):
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        context.update({'content': json.loads(Credential.objects.get(pk=self.kwargs['pk']).content)})
        return context


class CredentialCreateView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_create'
    model = Credential
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.issuer_id = self.request.user.id
        form.instance.owner_id = self.kwargs['pk']
        form.instance.status = 'created'
        return super(CredentialCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cert-credential-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(CredentialCreateView, self).get_context_data(**kwargs)
        context.update({'profile': Profile.objects.filter(user__id=self.kwargs['pk']).first()})
        return context
