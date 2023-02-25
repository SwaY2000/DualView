# Generated by Django 4.1.7 on 2023-02-24 22:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friend_requests_received',
            field=models.ManyToManyField(blank=True, related_name='user_friend_requests_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='friend_requests_sent',
            field=models.ManyToManyField(blank=True, related_name='user_friend_requests_sent', to=settings.AUTH_USER_MODEL),
        ),
    ]