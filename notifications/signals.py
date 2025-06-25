from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from comments.models import Comment
from likes.models import Like
from follows.models import Follow
from messaging.models import Message

# COMMENT SIGNAL
@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.user:
        Notification.objects.create(
            recipient=instance.post.user,
            actor=instance.user,
            verb='commented on your post',
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.id
        )

# LIKE SIGNAL
@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.user:
        Notification.objects.create(
            recipient=instance.post.user,
            actor=instance.user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.id
        )

# FOLLOW SIGNAL
@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created and instance.follower != instance.following:
        Notification.objects.create(
            recipient=instance.following,
            actor=instance.follower,
            verb='started following you',
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.id
        )

# MESSAGE SIGNAL
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.receiver,
            actor=instance.sender,
            verb='sent you a message',
            target_content_type=ContentType.objects.get_for_model(instance),
            target_object_id=instance.id
        )
