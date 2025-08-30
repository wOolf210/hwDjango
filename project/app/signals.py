#signals
import logging

from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Bb,bb_custom_signal
logger= logging.getLogger(__name__)

@receiver(pre_delete,sender=Bb,dispatch_uid="bb_pre_delete_signal")
def bb_pre_delete(sender, instance, **kwargs):
    logger.info(f"{pre_delete} Bb title {instance.title}")

@receiver(post_delete,sender=Bb,dispatch_uid="bb_pre_delete_signal")
def bb_post_delete(sender, instance, **kwargs):
    logger.info(f"{post_delete} Bb title {instance.title}")

@receiver(bb_custom_signal, sender=Bb, dispatch_uid="bb_custom_signal_handler")
def bb_custom_handler(sender, instance, **kwargs):
    logger.info(f"Custom handler for {sender.__name__} with instance {instance.title}")


@receiver(pre_save,sender=Bb,dispatch_uid="bb_pre_save_signal")
def bb_pre_save(sender, instance, **kwargs):
    if instance.pk:
        orig=sender.objects.get(pk=instance.pk)
        logger.info(f"{pre_save} Bb title {orig.title}")
    else:
        logger.info(f"{pre_save} Bb title {instance.title}")

@receiver(post_save,sender=Bb,dispatch_uid="bb_post_save_signal")
def bb_post_save(sender, instance, created, **kwargs):
    action = "created" if created else "updated"
    logger.info(f"{post_save} Bb title {instance.title} Action: {action}")



def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User {user_logged_in} logged in Username: {user.username} Time:{timezone.now()}")


user_logged_in.connect(
    log_user_login,
    dispatch_uid="user_logged_in_signal"
)


# user_logged_in.disconnect(
#     log_user_login,
#     dispatch_uid="user_logged_in_signal"
# )