# myapp/urls.py
from django.urls import path
from .views import login_view, logout_view, submit_form, add_credentials,search_credentials,update_credential
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('submit_form/', submit_form, name='submit_form'),  # Accessible only to logged-in users
    path('add_credentials/', add_credentials, name='add_credentials'),
    path('search_credentials/', search_credentials, name='search_credentials'),
    path('update_credential/', update_credential, name='update_credential'),
    path('delete_credentials/', update_credential, name='delete_credentials'),
    

]
