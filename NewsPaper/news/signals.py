import os
from datetime import *
from django.utils import timezone

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Post


# @receiver(pre_save, sender= Post)
# def check_post_limit( sender, instance, **kwargs):
#     now = timezone.now()
#     if instance.pk:
#         return
#
#     start_time = now - timedelta(hours= 24)
#     recent_post_count = Post.objects.filter(
#         author=instance.author,
#         created_at__gte=start_time
#     ).count()
#
#     if recent_post_count >= 3:
#         raise  ValidationError("Нельзя пулбликовать более 3 новостей в сутки.")


@receiver(post_save, sender=Post)
def send_message_to_user(sender, instance, created, **kwargs):
    if created:
        print(f"Post created: {instance.title}")  # Отладка 1
        categories = instance.categories.all()
        print(f"Categories for post: {list(categories)}")
        for category in categories:
            print(f"Processing category: {category.name}")
            subscribers = category.subscribers.all()
            print(f"Subscribers for category {category.name}: {list(subscribers)}")
            for subscriber in subscribers:
                try:
                    print(f"Processing subscriber: {subscriber.username}")  # Отладка 5
                    print(f"Subscriber type: {type(subscriber)}")  # Отладка 6
                    print(f"Email attribute type: {type(subscriber.email)}")  # Отладка 7
                    print(f"Email value: {subscriber.email}")

                    email = subscriber.email
                    username = subscriber.username

                    subject = instance.title
                    html_content = f"""
                    <h2>Здравствуй, {username}.</h2>
                    <h3>Новая статья в твоём любимом разделе!</h3>
                    <h4>{instance.title}</h4>
                    <p>{instance.content[:50]}...</p>
                    """

                    send_mail(
                        subject=subject,
                        message="",
                        from_email=None,
                        recipient_list=[email],
                        html_message=html_content
                    )
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print("Конец")

