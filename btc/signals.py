from django.db.models.signals import post_save
from django.dispatch import receiver
from panel.models import RefferalProfile,Investors


@receiver(post_save, sender=Investors)
def create_profile(sender, instance, created, **kwargs):
    if created:
        RefferalProfile.objects.create(user=instance)


@receiver(post_save, sender=Investors)
def save_profile(sender, instance, **kwargs):
    instance.refferalprofile.save()