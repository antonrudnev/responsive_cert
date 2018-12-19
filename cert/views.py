from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.db.models import Q

from .models import Profile, Credential

import json
import re


class RedirectHomeView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_superuser:
            return redirect(to='admin:index')
        elif any(p in request.user.get_all_permissions()
                 for p in ['cert.view_issuer_profiles', 'cert.view_owner_profiles']):
            return redirect(to='cert-user-list')
        else:
            return redirect(to='cert-user-detail')


class UserListView(LoginRequiredMixin, ListView):

    def get_queryset(self):
        permissions_filter = []
        if self.request.user.has_perm('cert.view_issuer_profiles'):
            permissions_filter.append('issue_credentials')
        if self.request.user.has_perm('cert.view_owner_profiles'):
            permissions_filter.append('own_credentials')
        if permissions_filter:
            return Profile.objects.filter(user__groups__permissions__codename__in=permissions_filter)
        else:
            raise PermissionDenied


class UserDetailView(LoginRequiredMixin, DetailView):

    def is_your_profile(self):
        return self.get_user_id() == self.request.user.id

    def get_user_id(self):
        return int(self.kwargs.get('pk', None) or self.request.user.id)

    def get_object(self, **kwargs):
        try:
            profile = Profile.objects.get(pk=self.get_user_id())
            if ((self.request.user.has_perm('cert.view_owner_profiles') and
                 profile.user.has_perm('cert.own_credentials')) or
                (self.request.user.has_perm('cert.view_issuer_profiles')
                 and profile.user.has_perm('cert.issue_credentials'))) or self.is_your_profile():
                return profile
            else:
                raise PermissionDenied
        except Profile.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        q_filters = Q(owner__user_id=self.get_user_id())
        if not (self.request.user.has_perm('cert.view_all_credentials') or self.is_your_profile()):
            q_filters.add(Q(issuer__user_id=self.request.user.id), Q.AND)
        context.update({'owned_credentials': Credential.objects.filter(q_filters)})
        if self.request.user.has_perm('cert.view_all_credentials') or self.is_your_profile():
            context.update({'issued_credentials': Credential.objects.filter(issuer__user_id=self.get_user_id())})
        return context


class CredentialDetailView(LoginRequiredMixin, DetailView):

    def get_object(self, **kwargs):
        try:
            credential = Credential.objects.get(pk=self.kwargs['pk'])
            if (self.request.user.id in [credential.issuer_id, credential.owner_id] or
                    self.request.user.has_perm('cert.view_all_credentials')):
                return credential
            else:
                raise PermissionDenied
        except Credential.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CredentialDetailView, self).get_context_data(**kwargs)
        content = Credential.objects.get(pk=self.kwargs['pk']).content
        context.update({'content': json.loads(content if content else '{}')})
        return context


class CredentialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'cert.issue_credentials'
    template_name_suffix = '_create'
    model = Credential
    fields = ['title']

    def form_valid(self, form):
        form.instance.issuer_id = self.request.user.id
        form.instance.owner_id = self.kwargs['pk']
        form.instance.status = 'created'
        content = self.request.POST.dict()
        content.pop('csrfmiddlewaretoken', None)
        content.pop('title', None)
        form.instance.content = json.dumps(content)
        return super(CredentialCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('cert-credential-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        if not Profile.objects.get(pk=self.kwargs['pk']).user.has_perm('cert.own_credentials'):
            raise PermissionDenied
        context = super(CredentialCreateView, self).get_context_data(**kwargs)
        context.update({'owner_profile': Profile.objects.get(user__id=self.kwargs['pk'])})
        cert_template = Profile.objects.get(user__id=self.request.user.id).cert_template
        content_fields = re.findall(r'{{\s*content\.([A-Za-z0-9_]+)\s*}}', cert_template)
        context.update({'content_fields': content_fields})
        return context
