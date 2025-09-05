from django.contrib.auth.models import Group


def get_group(name):
    current_group = Group.objects.get(name=name)
    return current_group