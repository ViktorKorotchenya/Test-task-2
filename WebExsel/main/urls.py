from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DocumentAPIView

app_name = "main"

urlpatterns = [
    path("", views.uploadFile, name="uploadFile"),
    path("api/v1/documentlist", DocumentAPIView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
