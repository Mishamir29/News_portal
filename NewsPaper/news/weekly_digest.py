from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Article, Category

class Command(BaseCommand):
    help = 'Отправляет еженедельную рассылку новостей подписчикам'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)
        articles = Article.objects.filter(created_at__gte=week_ago)

        # Группируем статьи по категориям
        category_articles = {}
        for article in articles:
            category_articles.setdefault(article.category, []).append(article)

        sent_count = 0
        for subscription in Subscription.objects.select_related('user', 'category'):
            category = subscription.category
            if category in category_articles:
                articles_list = category_articles[category]
                article_links = "\n".join([
                    f"- {a.title}: {a.get_absolute_url()}"
                    for a in articles_list
                ])

                send_mail(
                    subject=f'Еженедельная подборка статей: {category.name}',
                    message=f"""Привет, {subscription.user.username}!

За последнюю неделю в категории "{category.name}" появились следующие статьи:

{article_links}

Не пропустите следующие новости — подпишитесь на обновления!

С уважением,
Команда NewsPortal""",
                    from_email='noreply@yournewsportal.com',  # Замени на реальный email
                    recipient_list=[subscription.user.email],
                    fail_silently=False,
                )
                sent_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Успешно отправлено {sent_count} еженедельных рассылок.')
        )