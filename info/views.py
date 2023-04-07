from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect
from django.urls import reverse
from .services.business_logic import get_crypto_data_from_coin_gecko


class WelcomePage(TemplateView):
    template_name = "welcome_page.html"


class Info10CoinsPage(ListView):
    template_name = "info_10_coins_page.html"
    # по этому имени мы будем обращаться к этому списку в html файле
    context_object_name = "crypto_info"

    """если пользователь авторизирован, то он может попасть
    только на info_250_coins_page и welcome_page, на
    info_10_coins_page попасть не может"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('welcome_page'))
        return super().dispatch(request, *args, **kwargs)

    """возвращает список данных, состоящий из словарей,
    где каждый словарь - информация об одной криптомонете.
    далее этот список используется в файле html в теге for
    False возвращает список 10 монет
    True возвращает список 250 монет"""

    def get_queryset(self):
        return get_crypto_data_from_coin_gecko(False)


class Info250CoinsPage(ListView):
    template_name = "info_250_coins_page.html"
    context_object_name = "crypto_info"
    # количество монет на одной странице
    paginate_by = 25

    """функция не позволяет открыть страницу info_250_coins_page,
    если пользователь не авторизирован"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # reverse позволяет использовать сокращенное имя, а не путь
            return redirect(reverse('welcome_page'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            filtered_list = list(
                filter(lambda d: d.get('name').lower() in search_query.lower() or d.get(
                    'symbol').lower() in search_query.lower(),
                       get_crypto_data_from_coin_gecko(True, 'market_cap')))
            if filtered_list:
                return filtered_list
        sorting = self.request.GET.get('sorting')
        if sorting:
            return get_crypto_data_from_coin_gecko(True, sorting)
        return get_crypto_data_from_coin_gecko(True, 'market_cap')
