from django.contrib import admin
from .models import Profile, Credential


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'organization', 'has_public_key', 'has_private_key', 'has_cert_template')
    sortable_by = ('description', 'organization')
    ordering = ('user__username', )


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Credential)
