# Generated by Django 5.1.6 on 2025-03-12 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customuser_role_customuser_role_selected_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_login',
            field=models.BooleanField(default=True),
        ),
    ]
