from django.contrib import admin

from .  import custom_admin_form
from . import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import secrets
import string
import re

class UserAdmin(BaseUserAdmin):
    add_form = custom_admin_form.CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    actions = ['create_user_with_password']

    def create_user_with_password(self, request, queryset):
        for user_data in queryset:
            username = user_data.username
            email = user_data.email
            if not username:
                self.message_user(request, "Username is required.", level='ERROR')
                return
            if len(username) > 150:
                self.message_user(request, "Username must be 150 characters or fewer.", level='ERROR')
                return
            if not re.match(r'^[\w.@+-]+$', username):
                self.message_user(request, "Username can only contain letters, digits, and @/./+/-/_", level='ERROR')
                return
            if User.objects.filter(username=username).exists():
                self.message_user(request, f"Username {username} is already taken.", level='ERROR')
                return
            if not email:
                self.message_user(request, "Email is required.", level='ERROR')
                return

            password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(12))
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )
            doctor_group, _ = Group.objects.get_or_create(name='Doctor')
            user.groups.add(doctor_group)

            subject = 'Your CEMA Health System Account Password'
            message = f"""
                Hello {user.first_name},

                Your account has been created for the Health System application.
                Below are your login details:

                Username: {user.username}
                Password: {password}
                Email: {user.email}

                Regards,
                CEMA Health System Team
                """
            send_mail(subject, message, 'accounts@havenke.com', [user.email], fail_silently=False)
            self.message_user(request, f"User {username} created and password emailed.")
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(models.HealthProgram)
