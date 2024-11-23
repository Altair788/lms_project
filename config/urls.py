from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("lms.urls", namespace="lms")),
    path("users/", include("users.urls", namespace="users")),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
