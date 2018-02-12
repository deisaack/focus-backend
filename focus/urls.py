from django.contrib import admin
from django.urls import path, include
from focus.apps.accounts import urls as acc_urls
from focus.apps.documents import urls as doc_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(acc_urls)),
    path('documents/', include(doc_urls)),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
