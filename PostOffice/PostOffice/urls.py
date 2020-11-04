import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from home.views import *

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
]
