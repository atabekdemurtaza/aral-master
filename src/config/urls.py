from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="GreenAralSea API",
      default_version='v1',
      description="API for GreenAralSea.org website",
      terms_of_service="https://www.greenaralsea.org/terms/",
      contact=openapi.Contact(email="contact@greenaralsea.org"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/', include('api.urls'), name='api'),
    path('api-auth/', include('rest_framework.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    [
        re_path('^.*', TemplateView.as_view(template_name='index.html'))
    ]

urlpatterns += [
    re_path('^$', lambda request: HttpResponseRedirect('/swagger/'))
]