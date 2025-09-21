from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.db import transaction
from .models import Post


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
@receiver(m2m_changed, sender=Post.categories.through)
def send_article_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        print(f'Сигнал m2m_changed для статьи {instance.title}!')
        print(f'Добавленные категории ID: {pk_set}')
        print(f'Все категории статьи: {list(instance.categories.all())}')

        # Импортируем здесь чтобы избежать circular imports
        from .models import Category

        # Отправляем уведомления для добавленных категорий
        for category_id in pk_set:
            try:
                category = Category.objects.get(id=category_id)
                subscribers = category.subscribers.all()
                print(f'Подписчики категории {category.name}: {subscribers.count()}')

                for user in subscribers:
                    try:
                        send_mail(
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
                        print(f"Письмо отправлено для {user.email}")
                    except Exception as e:
                        print(f"Ошибка отправки email для {user.email}: {e}")

            except Category.DoesNotExist:
                print(f"Категория с ID {category_id} не найдена")


# @receiver(post_save, sender=Post)
# def send_message_to_user(sender, instance, created, **kwargs):
#     if created:
#         categories = instance.categories.all()
#         for category in categories:
#             subscribers = category.subscribers.all()
#             for subscriber in subscribers:
#                 try:
#                     email = subscriber.email
#                     username = subscriber.username
#
#                     subject = instance.title
#                     html_content = f"""
#                     <h2>Здравствуй, {username}.</h2>
#                     <h3>Новая статья в твоём любимом разделе!</h3>
#                     <h4>{instance.title}</h4>
#                     <p>{instance.content[:50]}...</p>
#                     """
#
#                     send_mail(
#                         subject=subject,
#                         message="",
#                         from_email=None,
#                         recipient_list=[email],
#                         html_message=html_content
#                     )
#                 except Exception as e:
#                     import traceback
#                     traceback.print_exc()
#                     print("Конец")

