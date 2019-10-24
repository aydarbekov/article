from django.urls import path
from accounts.views import login_view, logout_view

urlpatterns = [
    path('accounts/login', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
]

app_name = 'accounts'
