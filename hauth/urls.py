from django.urls import path
from hauth.views import LoginView,RegisterView,LogoutView
from . import views

app_name = 'hauth'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/',views.send_captcha,name='send_mail'),
    path('logout/',LogoutView.as_view() ,name='logout'),
]
