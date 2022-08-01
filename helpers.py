from flask import redirect, render_template, request, session
from functools import wraps
import requests

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


exchange_rate = {
    "usd_to_uah": 29.55,
    "usd_to_eur": 0.9809,
    "uah_to_usd": 0.03384095,
    "uah_to_eur": 0.03607538,
    "eur_to_uah": 30.4628,
    "eur_to_usd": 1.0191603,
}
try:    
    usd_to_uah = float(requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=UAH&apikey="KVRY6LAP4SU05Q6Z"').json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    if usd_to_uah == exchange_rate['usd_to_uah']:
        pass
    else:
        exchange_rate['usd_to_uah'] = usd_to_uah
except KeyError:
    pass
try:    
    usd_to_eur = float(requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=EUR&apikey="KVRY6LAP4SU05Q6Z"').json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    if usd_to_eur == exchange_rate['usd_to_eur']:
        pass
    else:
        exchange_rate['usd_to_eur'] = usd_to_eur
except KeyError:
    pass
try:        
    uah_to_usd = float(requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=UAH&to_currency=USD&apikey="KVRY6LAP4SU05Q6Z"').json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    if uah_to_usd == exchange_rate['uah_to_usd']:
        pass
    else:
        exchange_rate['uah_to_usd'] = uah_to_usd
except KeyError:
    pass
try:    
    uah_to_eur = float(requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=UAH&to_currency=EUR&apikey="KVRY6LAP4SU05Q6Z"').json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    if uah_to_eur == exchange_rate['uah_to_eur']:
        pass
    else:
        exchange_rate['uah_to_eur'] = uah_to_eur
except KeyError:
    pass
try:    
    eur_to_uah = float(requests.get('https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=UAH&apikey="KVRY6LAP4SU05Q6Z"').json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
    if eur_to_uah == exchange_rate['eur_to_uah']:
        pass
    else:
        exchange_rate['eur_to_uah'] = eur_to_uah
except KeyError:
    pass
try:    
    eur_to_usd = float(1/exchange_rate['usd_to_eur'])
    if eur_to_usd == exchange_rate['eur_to_usd']:
        pass
    else:
        exchange_rate['eur_to_usd'] = eur_to_usd
except KeyError:
    pass

# exchange_rate = {
#     "usd_to_uah": usd_to_uah,
#     "usd_to_eur": usd_to_eur,
#     "uah_to_usd": uah_to_usd,
#     "uah_to_eur": uah_to_eur,
#     "eur_to_uah": eur_to_uah,
#     "eur_to_usd": eur_to_usd,
# }