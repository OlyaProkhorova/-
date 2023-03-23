from django.shortcuts import render

from django.views.generic import TemplateView

# Create your views here.

class WelcomePage(TemplateView):
    template_name = "welcome_page.html"
