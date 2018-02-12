from __future__ import absolute_import
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'file', views.FileViewSet, base_name='file')
router.register(r'approval', views.ApprovalViewSet, base_name='approval')

app_label = 'documents'
# urlpatterns = [
#     path('signup/', views.UserCreateView.as_view(), name='signup'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('check_username/<str:username>/', views.check_username, name='check_username'),
#     path('check_email/', views.check_email, name='check_email'),
#     re_path('activate/<uuid:uidb64>/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
#            views.activate, name='activate'),
# ]

urlpatterns = router.urls
