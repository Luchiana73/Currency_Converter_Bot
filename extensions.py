import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIException(f'- Валюты должны быть разными. Сейчас вы ввели: {base} и {quote}.')

        errors = []
        base_ticker = ""
        quote_ticker = ""

        try:
            base_ticker = keys[base]
        except KeyError:
            errors.append(f'- Не удалось обработать валюту: {base}. Пожалуйста, проверьте правильность написания.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            errors.append(f'- Не удалось обработать валюту: {quote}. Пожалуйста, проверьте правильность написания.')
        try:
            amount = float(amount)
            if amount < 0:
                errors.append(f'- Сумма не может быть меньше нуля. Сейчас вы ввели {amount}.')
        except ValueError:
            errors.append(f'- Сумма ({amount}) должна быть введена в числовом формате.')

        if errors:
            raise APIException('\n'.join(errors))

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        rate = json.loads(r.content)[quote_ticker]
        total_base = rate * amount
        return total_base
