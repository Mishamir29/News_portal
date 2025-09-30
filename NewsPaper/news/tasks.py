from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta

from pyexpat.errors import messages

from .models import Post, Category


@shared_task
def send_notification_new_post(post_id):
    print(f"✅ Задача запущена! post_id = {post_id}")
    try:
        post = Post.objects.get(id=post_id)
        if post.post_type != Post.NEWS:
            return "Это не новость - рассылка не требуется"

        categories = post.categories.all()
        if not categories.exists():
            return "Новость без категорий - рассылка невозможна"

        subscribers_emails = set()
        for category in categories:
            for user in category.subscribers.all():
                if user.email:
                    subscribers_emails.add(user.email)

        if not subscribers_emails:
            return "Нет подписчиков с email"

        subject = f"Новая новость: {post.title}"
        message = (
            f"Заголовок: {post.title}\n"
            f"Превью: {post.preview()}\n"
            f"Полный текст: http://127.0.0.1:8000{post.get_absolute_url()}"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=list(subscribers_emails),
            fail_silently=False,
        )
        return f"Уведомление отправлено {len(subscribers_emails)} подписчикам"
    except Post.DoesNotExist:
        return "Пост не найден"


@shared_task
def send_weekly_newsletter():
    week_ago = timezone.now() - timedelta(days=7)
    news_posts = Post.objects.filter(
        post_type=Post.NEWS,
        created_at__gte=week_ago
    ).order_by('-created_at')

    if not news_posts.exists():
        return "Нет новостей за неделю"


    all_subscribers = set()
    for post in news_posts:
        for category in post.categories.all():
            for user in category.subscribers.all():
                if user.email:
                    all_subscribers.add(user.email)

    if not all_subscribers:
        return "Нет подписчиков для еженедельной рассылки"

    news_list = "\n\n".join([
        f"Что-то новое! {post.title}\n{post.preview()}\nЧитать: http://127.0.0.1:8000{post.get_absolute_url()}"
        for post in news_posts
    ])
    subject = "Еженедельная подборка новостей"
    message = f"Вот что вышло за послюднюю неделю:\n\n{news_list}"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=list(all_subscribers),
        fail_silently=False,
    )
    return f"Еженедельная рассылка отправлена {len(all_subscribers)} пользователям"