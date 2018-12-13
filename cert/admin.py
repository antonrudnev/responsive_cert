from django.contrib import admin
from .models import Profile, Credential


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'description', 'organization',
                    'has_public_key', 'has_private_key', 'has_cert_template')
    ordering = ('user__username', )

    def has_public_key(self, obj):
        return True if obj.public_key else False

    has_public_key.boolean = True

    def has_private_key(self, obj):
        return True if obj.private_key else False

    has_private_key.boolean = True

    def has_cert_template(self, obj):
        return True if obj.cert_template else False

    has_cert_template.boolean = True

    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" \
            if obj.user.first_name and obj.user.last_name \
            else obj.user.username

    user_name.short_description = 'user'
    user_name.admin_order_field = 'user__username'


class CredentialAdmin(admin.ModelAdmin):
    list_display = ('owner', 'organization', 'title', 'created_on', 'has_transaction_id', 'status')
    ordering = ('owner__user__username',)

    def organization(self, obj):
        return obj.issuer.organization

    organization.admin_order_field = 'issuer__organization'

    def has_transaction_id(self, obj):
        return True if obj.transaction_id else False

    has_transaction_id.boolean = True


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Credential, CredentialAdmin)
