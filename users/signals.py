# users/signals.py

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == 'users':  # Only run for the 'users' app
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        user_group, _ = Group.objects.get_or_create(name='User')

        admin_permissions = Permission.objects.filter(
            content_type__app_label='auth',
            codename__in=['change_user', 'view_user']
        )
        admin_group.permissions.set(admin_permissions)
