from django.contrib import admin
from django.contrib.messages import api
from django.urls import path, include
from django.conf.urls.static import static
from config import settings
from config.settings import MEDIA_URL
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('Olcha/', include('olcha.urls'), name='olcha'),

    # API
    path('api-token-auth/', views.obtain_auth_token),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

] + static(MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]