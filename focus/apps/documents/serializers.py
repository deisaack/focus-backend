from __future__ import absolute_import
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import File, Approval
from focus.apps.accounts.serializers import UserSerializer

User=get_user_model()


class ApprovalsSerializer(serializers.ModelSerializer):
    user=UserSerializer(required=False)

    class Meta:
        model = Approval
        fields = ('user', 'file')


class FileSerializer(serializers.ModelSerializer):
    approval_count = serializers.SerializerMethodField()
    # approvals = ApprovalsSerializer(many=True, required=False)

    class Meta:
        model = File
        fields = ('id', 'user', 'detail', 'item', 'approval_count', )
        # fields = ('user', 'detail', 'item', 'approval_count', 'approvals')
        read_only_fields=('user', )

    def get_approval_count(self, obj):
        return Approval.objects.filter(file=obj).count()

