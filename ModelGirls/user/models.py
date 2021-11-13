from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib import auth


class Profile(models.Model):
    user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to='image')
    nickname = models.CharField(max_length=40, blank=True)
    bio = models.TextField(blank=True)


def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
