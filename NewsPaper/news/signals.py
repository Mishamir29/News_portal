from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.shortcuts import redirect


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def add_user_to_common_group(sender, instance, created, **kwargs):
    """
    Добавляет нового пользователя в группу 'common' после регистрации.
    """
    if created:  # Проверяем, что пользователь только что создан
        try:
            common_group = Group.objects.get(name='common')
            instance.groups.add(common_group)
        except Group.DoesNotExist:
            # Можно залогировать ошибку, если группа 'common' не существует
            print("Группа 'common' не найдена. Пользователь не добавлен.")
            pass
