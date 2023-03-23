from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect
from django.urls import reverse
from .services.business_logic import get_crypto_data_from_coin_gecko


class WelcomePage(TemplateView):
    template_name = "welcome_page.html"


class Info10CoinsPage(ListView):
    template_name = "info_10_coins_page.html"
    context_object_name = "crypto_info"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('welcome_page'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_crypto_data_from_coin_gecko(False)

