from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    path('', include('accounts.urls'))
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
]

