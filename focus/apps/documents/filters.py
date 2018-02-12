from django_filters import rest_framework as filters
from .models import File
from django.contrib.auth import get_user_model

User = get_user_model()


class FileFilter(filters.FilterSet):
    class Meta:
        model = File
        fields = (
            'user',
        )