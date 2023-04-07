from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import transaction


class AuthorizationTests(TestCase):
    # создает тестового пользователя
    def setUp(self):
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'password'
        self.user = User.objects.create_user(username=username, email=email, password=password)

    # проверяет, что по указанному пути существует страница входа
    def test_login_page_exists(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    # проверяет, что по указанному пути существует страница регистрации
    def test_signup_page_exists(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    # проверяем, добавился ли пользователь в БД и правильно ли добавились его данные
    def test_user_registration(self):
        user_count = User.objects.filter(username=self.user.username).count()
        self.assertEqual(user_count, 1)
        user = User.objects.get(username=self.user.username)
        self.assertEqual(user.email, self.user.email)

    # проверяет, что после регистрации пользователя перенаправляет на страницу info_250_coins
    def test_signup_redirects_to_250_coins_page(self):
        # используется для частей кода, которые обращаются к базе данных
        with transaction.atomic():
            signup_data = {'username': 'testuser1', 'email': 'testuser@example.com', 'password': 'testpass123'}
            response = self.client.post(reverse('signup'), data=signup_data)
            self.assertRedirects(response, reverse('info_250_coins'))

    # проверяет, что при входе в аккаунт пользователя перенаправляет на страницу info_250_coins
    def test_login_redirects_to_250_coins_page(self):
        with transaction.atomic():
            login_data = {'username': 'testuser', 'pass': 'password'}
            response = self.client.post(reverse('login'), data=login_data)
            self.assertRedirects(response, reverse('info_250_coins'))

    # удаляется тестовый пользователь из бд
    def tearDown(self):
        self.user.delete()