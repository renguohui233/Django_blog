from django import http
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.http.response import JsonResponse
from django.core.mail import send_mail
import random
import string
from .models import CaptchaModel

from .forms import RegisterForm,LoginForm
from django.contrib.auth import get_user_model,login,logout


User = get_user_model()


# Create your views here.
class LoginView(View):
    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password =form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            print(remember)
            user = User.objects.filter(username=username).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
        else:
            return redirect(reverse('hauth:login'))

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')



class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('hauth:login'))
        else:
            print(form.errors)
            # 重新跳转到登录页面
            return redirect(reverse('hauth:register'))
            # return render(request, 'register.html', context={"form": form})


def send_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'msg': '必须填写邮箱'})
    captcha = "".join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={"captcha": captcha})
    send_mail('邮箱验证码', message=f"您的验证码: {captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'msg': '验证码发送成功'})
