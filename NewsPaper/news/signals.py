from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Post, Category
from .tasks import send_notification_new_post


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject="Добро пожаловать в NewsPortal!",
            message=f"""Здравствуйте, {instance.username}!

Спасибо за регистрацию в нашем новостном портале.

Теперь вы можете подписываться на любимые категории новостей — и получать еженедельные подборки прямо на почту.

С уважением,
Команда NewsPortal""",
            from_email='jaroslav.cukushik@yandex.ru',
            recipient_list=[instance.email],
            fail_silently=False,
        )

# Письмо при добавлении новой статьи
@receiver(m2m_changed, sender=Post)
def send_article_notification(sender, instance, created, pk_set, **kwargs):
    if created:
        print(f'Сигнал есть от статьи {instance.title}!')
        # Отправляем письма всем подписчикам категорий статьи
        for category_id in pk_set:
            print(f'список {instance.categories}')
            category = Category.objects.get(id=category_id)
            subscribers = category.subscribers.all()
            for user in subscribers:
                try: send_mail(
                    subject=f'Новая статья в "{category.name}"',
                    message=f"""Здравствуйте, {user.username}!

Появилась новая статья в категории "{category.name}":

{instance.title}

{instance.content[:200]}...

Читать полностью: http://127.0.0.1:8000{instance.get_absolute_url()}

С уважением,
Команда NewsPortal""",
                    from_email='jaroslav.cukushik@yandex.ru',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                except Exception as e:
                    print(f"Ошибка отправки email: {e}")


@receiver(post_save, sender=Post)
def notify_subscribers_on_news_creation(sender, instance, created, **kwargs):
    if created and instance.post_type == Post.NEWS:
        send_notification_new_post.delay(instance.id)