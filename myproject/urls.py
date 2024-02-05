# myproject/urls.py
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from myapp.views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False), name='home'),
    path('myapp/', include('myapp.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
