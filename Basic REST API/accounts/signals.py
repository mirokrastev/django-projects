from django.dispatch import receiver
from django.db.models import signals
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


@receiver(signal=signals.post_save, sender=UserModel)
def generate_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
