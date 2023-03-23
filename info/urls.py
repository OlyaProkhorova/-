from django.urls import path
from .views import WelcomePage

urlpatterns = [
    path("", WelcomePage.as_view(), name="welcome_page")
]