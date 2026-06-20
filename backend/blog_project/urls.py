from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"})


def readiness_check(request):
    return JsonResponse({"status": "ready"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('blog.urls')),
    path('health/', health_check, name='health'),
    path('readiness/', readiness_check, name='readiness'),
]
