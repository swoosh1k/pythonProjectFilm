import time

from celery import shared_task
from django_movie.celery import app
import datetime

def print_time():
    now = datetime.datetime.now()
    print("Current time is:", now)






@app.task
def print_time_task():
    print_time()


@app.task
def go_binance():
    import json
    import requests

    # Defining Binance API URL
    key = "https://api.binance.com/api/v3/ticker/price?symbol="

    # Making list for multiple crypto's
    currencies = ["BTCUSDT", "DOGEUSDT", "LTCUSDT"]
    j = 0

    # running loop to print all crypto prices
    for i in currencies:
        # completing API for request
        url = key + currencies[j]
        data = requests.get(url)
        data = data.json()
        j = j + 1
        print(f"{data['symbol']} price is {data['price']}")



@shared_task
def add(x, y):
    print('привет питонисты ызпоыпызпызщпыщз')
    return x + y







print_time_task.delay()
print(add.delay(1, 45))
go_binance.delay()
