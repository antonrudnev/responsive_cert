from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='cert-user-list'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='cert-user-detail'),
    path('users/<pk>/credentials/', views.CredentialListView.as_view(), name='cert-user-credential-list'),
    path('credentials/<pk>/', views.CredentialDetailView.as_view(), name='cert-credential-detail'),
]
