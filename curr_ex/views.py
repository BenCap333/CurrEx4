from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from curr_ex.models import Currency
from curr_ex.models import Rates
from datetime import datetime
import request



#import currency
from django.utils import functional


#home, scraping, rate functions
#
# def home(request):
#     data = dict()
#     return render(request,"home.html",context=data)


def home(request):
    data = dict()
    if request.GET and "symbol" in request.GET:
        iso_code = request.GET['symbol']
        try:
            symbol_list = get_currency_rates(iso_code)
            print(symbol_list)
        except:
            data['error'] = True
            data['symbol'] = iso_code
            return render(request,"home.html",context=data)
    else:
        return render(request, "home.html")


from curr_ex.models import Currency
from curr_ex.models import Rates

# def symbol_error(request):
#     return HttpResponseRedirect(reverse(''))

def get_currency_rates(iso_code): #scrapes
    url = "http://www.xe.com/currencytables/?from=" + iso_code
    import requests
    from bs4 import BeautifulSoup
    x_rate_list = list()
    try:
        page_source = BeautifulSoup(requests.get(url).content, 'html.parser')
    except:
        return x_rate_list
    data = page_source.find('tbody')
    data_lines = data.find_all('tr')
    for line in data_lines:
        data = line.find_all('td')
        try:
            x_currency = data[0].get_text().strip()
            x_rate = float(data[2].get_text().strip())
            x_rate_list.append((x_currency, x_rate))
        except:
            continue
    return x_rate_list


def rates(request):
    symbol = request.GET("symbol")
    try:
        result_list = get_currency_rates(symbol)
        print(result_list)
        try:
            Currency.objects.get(symbol=symbol)
        except:
            #create new record for this currency
            c = Currency()
            c.symbol = symbol
            c.save()
        for r in result_list:
            try:
                my_rate = Rates.objects.get(currency=symbol, x_currency=r[0])#get the record for this element, returns tuple
                my_rate.rate = r[1]
                my_rate.last_update_time = datetime.now()
                my_rate.save()
                #update r with the web scraping result

            except: # no record for element
                nr = Rates()
                nr.rate = rate
                nr.save()

        result = Rates.objects.filter(currency=symbol)
        data = dict()
        data['result'] = result
        return render(request, "rate.html",context=data)
    except:
        data = dict()
        data['error'] = True
        return render(request, "home.html")


