from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core import urls as core_urls

schema_view = get_schema_view(
   openapi.Info(
      title='Bill Indonesia Interview Test',
      default_version='v1',
      description='REST API for Bill Indonesia Interview Test',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include([
        path('', include(core_urls.urlpatterns), name='Core API')
    ]))
]
