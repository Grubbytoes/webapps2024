from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

RATES = {
    "USD": 0.8,
    "EUR": 0.9,
    "GBP": 1.0
}

@api_view()
def conversion_request(request):
    # Get the fields from the request
    currency_from = request.GET.get('from', "GBP")
    currency_to = request.GET.get('to', "GBP")
    amount = float(request.GET.get('amount', 0.0))
    value = convert(currency_from, currency_to, amount)
    return Response({"value": value})

def convert(currency_from, currency_to, amount):
    rate = RATES.get(currency_from, 1.0) / RATES.get(currency_to, 1.0)
    value = amount * rate
    print(value)
    return value
