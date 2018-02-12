from __future__ import absolute_import, unicode_literals
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.generics import views
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import AllowAny
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from decouple import config
from . import serializers as sz
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from . import filters as ft
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser, FormParser

from rest_framework.permissions import AllowAny
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes
)
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import (
    status,
    permissions
)
from .models import Employee
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activation_token
from django.shortcuts import redirect
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('accounts/emails/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate Your ElgonHub Account.'
            to_email = user.email
            to = [to_email]
            # activate_account.delay(mail_subject, message, to)
            # activate_account.delay(122)

            if user:
                employee, created = Employee.objects.get_or_create(user=user)
                employee.save()
                json = serializer.data
                payload = jwt_payload_handler(user)
                json['token'] = jwt_encode_handler(payload)
                json['messages'] = 'Please verify your email to continue'
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_200_OK)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validate_email(serializer.data['username'])
                valid_email = True
            except:
                valid_email = False

            if valid_email:
                try:
                    user = User.objects.get(email__iexact=serializer.data['username'])
                except:
                    user = None
            else:
                try:
                    user = User.objects.get(username__iexact=serializer.data['username'])
                except:
                    user = None
            if user is not None:
                if user.is_active:
                    login(request, user)
                    json = {}
                    json['email'] = user.email
                    json['first_name'] = user.first_name
                    json['last_name'] = user.last_name
                    json['image'] = request.scheme + '://' + self.request.META.get('HTTP_HOST') + user.employee.get_picture
                    json['username'] = serializer.data['username']
                    payload = jwt_payload_handler(user)
                    json['token'] = jwt_encode_handler(payload)
                    return Response(json, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "User is inactive. Please consult system admin"},
                                    status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def check_username(request, username):
    users = User.objects.filter(username__iexact=username)
    exists = False
    if users:
        exists = True
    return Response(exists, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def check_email(request):
    email = request.data[0]
    users = User.objects.filter(email=email)
    exists = False
    if users:
        exists = True
    return Response(exists, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def activate(request, uidb64, token):
    data = {}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        data['messages'] = 'Thank you for your email confirmation. Now you can login your account.'
        return redirect(config('LOGIN_URL'), data)
        # return Response(data, status=status.HTTP_202_ACCEPTED)
    else:
        data['messages'] = 'The activation link is invalid'
        return Response(data, status=status.HTTP_403_FORBIDDEN)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = sz.EmployeeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = ft.EmployeeFilter
    permission_classes = (AllowAny,)
    search_fields = ('employee_no', 'id_no', 'phone',)
    ordering_fields = ('phone_verified', 'created')
    ordering = ('-created')
    parser_classes = (MultiPartParser, FormParser, JSONParser)

