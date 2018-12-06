from django.contrib import admin
from .models import Profile, Credential


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'description', 'organization', 'has_public_key', 'has_private_key', 'has_cert_template')
    ordering = ('user__username', )

    def has_public_key(self, obj):
        return obj.public_key is not None

    has_public_key.boolean = True

    def has_private_key(self, obj):
        return obj.private_key is not None

    has_private_key.boolean = True

    def has_cert_template(self, obj):
        return obj.cert_template != ''

    has_cert_template.boolean = True

    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" \
            if obj.user.first_name and obj.user.last_name \
            else obj.user.username

    user_name.short_description = 'user'
    user_name.admin_order_field = 'user__username'


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Credential)
