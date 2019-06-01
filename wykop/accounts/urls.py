from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from wykop.accounts.views import BanedView, RegistrationView

app_name = 'accounts'


urlpatterns = [
    path('login', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('rejestracja', RegistrationView.as_view(), name='register'),
    path('banowanie/<int:user_pk>', BanedView.as_view(), name='ban'),
]
