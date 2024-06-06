from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(pre_save, sender=Profile)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = f'{instance.first_name}_{instance.last_name}'.lower()
        counter = 1
        while Profile.objects.filter(username=username):
            username = f'{instance.first_name}_{instance.last_name}_{counter}'.lower()
            counter += 1
        instance.username = username
    