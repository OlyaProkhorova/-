import requests
import json
import copy
from apscheduler.schedulers.background import BackgroundScheduler

""""здесь происходит первая загрузка данных c API CoinGecko.
Если этого не сделать, то сайт отобразит ошибку, так как 
список будет пустым. Это произойдет потому, что поток,
отвечающий за обновление списка криптовалют,
запустится только через 10 секунд. """
__path = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C7d&locale=en'
__response = requests.get(__path).json()
# преобразуем json в строку
__data = json.dumps(__response)
# преобразуем json строку в список, состоящий из словарей
__data = json.loads(__data)


# эта функция вызывается каждые 10 секунд и обновляет список с данными
def request_data_from_coin_gecko_api():
    global __data
    global __path
    response = requests.get(__path).json()
    __data = json.dumps(response)
    __data = json.loads(__data)


"""многопоточность применена с целью обойти ограничение API сайта CoinGecko,
т.к. бесплатная версия API предоставляет только 10-30 запросов в минуту. Если
превысить лимит по запросам, то сайт API возвращает предупреждение о превышение
запросов и сайт временно перестает работать. Поэтому в целях избежать данной
проблемы, список обновляется каждые 10 секунд, совершая только 6 запросов в минуту"""

# объект этого класса будет запускать функцию request_data_from_coin_gecko_api
# по расписанию каждые 10 секунд
scheduler = BackgroundScheduler()
scheduler.add_job(request_data_from_coin_gecko_api, 'interval', seconds=10)
scheduler.start()


# функция возвращает разные списки в зависимости от авторизации пользователя:
# для авторизированнных - 250 монет,
# для неавторизированных - 10 монет
def get_crypto_data_from_coin_gecko(user_is_authorized, sorting=None):
    return get_250_coins(sorting) if user_is_authorized else get_10_coins()


def get_10_coins():
    global __data
    # список будет содержать информацию о 10 монетах вместо 250,
    # как в исходном списке
    list_10_coins = []
    for index in range(10):
        list_10_coins.append(__data[index])
    for info in list_10_coins:
        # преобразуем котировку и цену в более удобный и читабельный вид
        info['symbol'] = info['symbol'].upper()
        info['current_price'] = round(info['current_price'], 9)
    return list_10_coins


def get_250_coins(sorting):
    global __data
    # deepcopy используется, чтобы сделать независимую копию списка __data,
    # чтобы когда мы вносим в нем изменения, то они не отражались на исходном списке
    data = copy.deepcopy(__data)
    for info in data:
        # переменные созданы для дальнейшего удобства путем сокращения кода
        changes_for_1h = info['price_change_percentage_1h_in_currency']
        changes_for_24h = info['price_change_percentage_24h']
        changes_for_7d = info['price_change_percentage_7d_in_currency']
        # иногда могут прийти значения None, поэтому добавляем проверку, т.к.
        # мы ожидаем float
        changes_for_1h = changes_for_1h if changes_for_1h is not None else 0.0
        changes_for_24h = changes_for_24h if changes_for_24h is not None else 0.0
        changes_for_7d = changes_for_7d if changes_for_7d is not None else 0.0
        info["symbol"] = str(info['symbol']).upper()
        # округляем до 9 знаков после запятой, чтобы информация помещалась в форму
        info["current_price"] = round(info['current_price'], 9)
        # округляем до 1 знака после запятой для удобочитаемости
        info["price_change_percentage_1h_in_currency"] = round(changes_for_1h, 1)
        info["price_change_percentage_24h"] = round(changes_for_24h, 1)
        info["price_change_percentage_7d_in_currency"] = round(changes_for_7d, 1)
    # сортируем список криптовалют по выбранным значениям сортировки:
    # цена, объем торгов, изменения цен.
    # по умолчанию сортирует по рыночной капитализации
    # reverse=True сортирует по убыванию
    sorted_list = sorted(data, key=lambda d: d[sorting], reverse=True)
    # объем торгов приводим в удобно читаемый вид, разделяя разряды пробелами
    for info in sorted_list:
        volume = info['total_volume']
        info['total_volume'] = f'{volume:,}'.replace(',', ' ')
    return sorted_list
