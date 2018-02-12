from __future__ import absolute_import
from . import serializers as sz
from . models import File, Approval
from rest_framework import serializers
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from . import filters as ft
from rest_framework import viewsets


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = sz.FileSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ft.FileFilter
    search_fields = ('employee_no', 'id_no', 'phone',)
    ordering_fields = ('phone_verified', 'created')
    ordering = ('-created',)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        serializer.save(item=self.request.FILES.get('item'), user=self.request.user)


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = sz.ApprovalsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # filter_class = ft.FileFilter
    # search_fields = ('employee_no', 'id_no', 'phone',)
    ordering_fields = ('created',)
    ordering = ('-created',)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
