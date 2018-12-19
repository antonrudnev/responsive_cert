from django.urls import path

from . import views

urlpatterns = [
    path('', views.RedirectHomeView.as_view(), name='cert-home'),
    path('users/', views.UserListView.as_view(), name='cert-user-list'),
    path('users/<pk>/', views.UserDetailView.as_view(), name='cert-user-detail'),
    path('users/<pk>/issue/', views.CredentialCreateView.as_view(), name='cert-user-credential-create'),
    path('credentials/', views.UserDetailView.as_view(), name='cert-user-detail'),
    path('credentials/<pk>/', views.CredentialDetailView.as_view(), name='cert-credential-detail'),
]
