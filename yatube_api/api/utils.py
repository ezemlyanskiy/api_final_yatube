from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def get_common_slug(read_only=True):
    return serializers.SlugRelatedField(
        read_only=read_only,
        slug_field='username',
        default=serializers.CurrentUserDefault() if read_only else None,
        queryset=User.objects.all() if not read_only else None,
    )
