from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

"""Когда пользователь вводит данные и нажимает кнопку зарегистрироваться,
 отправляется запрос POST на сервер. В этой функции проверяем, что пришел
 POST запрос, далее получаем данные, введённые пользователем и создаем нового
 пользователя в БД. После регистрации сразу же выполняется вход в аккаунт 
 под новым пользователем и происходит переход на страницу 250coins"""


def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username != '' and password != '':
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('info_250_coins')
    # Функция render() загружает указанный шаблон,
    # после чего генерирует HTTP-ответ в виде объекта HttpResponse,
    # содержащего результат рендеринга шаблона.
    return render(request, 'registration/signup.html')


"""Когда пользователь вводит данные и нажимает кнопку войти,
 отправляется запрос POST на сервер. В этой функции проверяем, что пришел
 POST запрос, далее получаем данные, введённые пользователем и проверяем
 есть ли такой пользователь в БД, если есть, то входим в аккаунт пользователя. 
 Далее происходит переход на страницу 250coins"""


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('info_250_coins')
    return render(request, 'registration/login.html')


def logout_page(request):
    logout(request)
    return redirect('welcome_page')
