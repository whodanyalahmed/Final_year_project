from datetime import datetime
from xmlrpc.client import DateTime
from django.http import JsonResponse
from scrapper_and_analyzer.models import Dataset
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from django.template.defaulttags import register
import json
from numpy import Infinity
from scrapper_and_analyzer import urls
from scrapper_and_analyzer.backend.pakmobizone import pakmobizone_main
from scrapper_and_analyzer.backend.priceoye import priceOye_main
from scrapper_and_analyzer.backend.daraz import daraz_main
from django.urls import resolve
from django.shortcuts import redirect, render
import sys
from django.views.decorators.cache import cache_control
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression


sys.path.append('../')
# from ..models import Dataset


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def get_predicted_price(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        # new_date to 2023-12-31
        date = request.POST.get('date')
        # create datetime object
        new_date = datetime.strptime(date, '%Y-%m-%d')
        # reshape new_Date to 2d array
        new_date = np.reshape(new_date, (1, -1))
        # add to df
        new_date = pd.DataFrame(new_date)
        # convert to float
        print(new_date)
        # convert to date

        # select all the data with the keyword
        data = Dataset.objects.filter(name__contains=keyword)
        # searialize the data
        data = list(data.values())
        # # get the dataframe
        df = pd.DataFrame(data)
        print(df)
        y = df['price'].astype("float64")
        x = df['fetched_date'].dt.date
        # convert x to .astype("datetime64[ns]")
        x = x.astype("datetime64[ns]")
        print(x)
        # get date column
        # x = df['fetched_date'].astype("datetime64[ns]")
        # reshape the data
        x = x.values.reshape(-1, 1)
        y = list(y)
        # transpose y
        y = np.transpose(y)
        model = LinearRegression()
        model.fit(x, y)
        r_sq = model.score(x.astype('float64'), y)
        print(f"coefficient of determination: {r_sq}")
        print(f"intercept: {model.intercept_}")
        print(f"slope: {model.coef_}")
        # reshape new_date to 2d array
        new_date = new_date.values.reshape(-1, 1)
        new_date = [[float(new_date)]]
        print(new_date)
        y_pred = model.predict(new_date)
        print(f"predicted response:\n{y_pred}")
        print(f"actual response:\n{y}")
        y_pred = json.dumps(y_pred, cls=NumpyEncoder)

        return JsonResponse(y_pred, safe=False)


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):

    current_url = resolve(request.path_info).url_name
    return render(request, 'index.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Minimum(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'minimum.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def maximum(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'maximum.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def _list(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'list.html', context={'current_url': current_url})


@ cache_control(no_cache=True, must_revalidate=True, no_store=True)
def prediction(request):
    current_url = resolve(request.path_info).url_name
    return render(request, 'prediction.html', context={'current_url': current_url})


def get_min_max_price(daraz, priceOye, pakmobizone):

    price_array = [daraz['price'],
                   priceOye['price'], pakmobizone['price']]
    lowest_price = min(price_array)
    # find the highest price
    highest_price = max(price_array)
    # get the index of the lowest price
    lowest_index = price_array.index(lowest_price)
    # get the index of the highest price
    highest_index = price_array.index(highest_price)
    if(lowest_index == 0):
        min_price_product = daraz
    elif(lowest_index == 1):
        min_price_product = priceOye
    else:
        min_price_product = pakmobizone

    if(highest_index == 0):
        max_price_product = daraz
    elif(highest_index == 1):
        max_price_product = priceOye
    else:
        max_price_product = pakmobizone
    return min_price_product, max_price_product


def result(request):
    # get browser session storage value

    # get request values
    if request.method == 'POST':

        keyword = request.POST.get('keyword')
        current_url = request.POST.get('url')
        print(keyword)
        if(not bool(keyword)):
            return render(request, 'results.html', context={'msg': "error", "text": "No keyword entered!"})
        else:
            # call scrapper function
            print("current_url: ", current_url)
            if (current_url != 'list'):
                try:
                    try:

                        priceOye = priceOye_main(keyword, "result")
                    except Exception as e:
                        print(e)
                        priceOye = {
                            "name": "No Product found",
                            "price": Infinity,
                            "src": "static/images/not_found.svg"
                        }
                    try:
                        daraz = daraz_main(keyword, "result")
                    except Exception as e:
                        print(e)
                        daraz = {
                            "name": "No Product found",
                            "price": Infinity,
                            "src": "static/images/not_found.svg"
                        }
                    try:

                        pakmobizone = pakmobizone_main(keyword, "result")
                    except Exception as e:
                        print(e)
                        pakmobizone = {
                            "name": "No Product found",
                            "price": Infinity,
                            "src": "static/images/not_found.svg"
                        }

                    if(daraz['name'] == "No Product found" and priceOye['name'] == "No Product found" and pakmobizone['name'] == "No Product found"):
                        return render(request, 'results.html', context={'msg': "error", "text": "No result found!"})

                    # find the lowest price

                    # set values in session
                    request.session['daraz'] = daraz
                    request.session['priceOye'] = priceOye
                    request.session['pakmobizone'] = pakmobizone
                    request.session['current_url'] = current_url
                    # if anyone is infinity
                    min_price_product, max_price_product = get_min_max_price(
                        daraz, priceOye, pakmobizone)
                    return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "pakmobizone": pakmobizone, "min_price_product": min_price_product, "max_price_product": max_price_product, "current_url": current_url})
                except Exception as e:
                    return render(request, 'results.html', context={'msg': "error", "text": "Can't find the product or may not exist!"})
            else:
                try:

                    priceOye = priceOye_main(keyword, "list")
                except:
                    priceOye = {"names": [], "prices": [],
                                "images": [], "links": []}
                try:
                    daraz = daraz_main(keyword, "list")
                except:
                    daraz = {"names": [], "prices": [],
                             "images": [], "links": []}
                try:

                    pakmobizone = pakmobizone_main(keyword, "list")
                except:
                    pakmobizone = {"names": [], "prices": [],
                                   "images": [], "links": []}

                request.session['daraz'] = daraz
                request.session['priceOye'] = priceOye
                request.session['pakmobizone'] = pakmobizone
                request.session['current_url'] = current_url

                return redirect('list_result')
    if request.method == 'GET':
        # get values fromm session
        try:

            current_url = request.session['current_url']
            daraz = request.session['daraz']
            priceOye = request.session['priceOye']
            pakmobizone = request.session['pakmobizone']
            if current_url != 'list':
                min_price_product, max_price_product = get_min_max_price(
                    daraz, priceOye, pakmobizone)
                return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "pakmobizone": pakmobizone, "min_price_product": min_price_product, "max_price_product": max_price_product, "current_url": current_url})

            else:
                return redirect('list_result')
        except:
            return redirect('Dashboard')


def list_results(request):
    # get values fromm session
    try:

        daraz = request.session['daraz']
        priceOye = request.session['priceOye']
        pakmobizone = request.session['pakmobizone']
        current_url = request.session['current_url']

        # daraz = json.dumps(daraz)
        # priceOye = json.dumps(priceOye)
        # pakmobizone = json.dumps(pakmobizone)
        # daraz range
        daraz_range = len(daraz['names'])
        # priceOye range
        priceOye_range = len(priceOye['names'])
        # pakmobizone range
        pakmobizone_range = len(pakmobizone['names'])

        return render(request, 'list_results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "pakmobizone": pakmobizone, "current_url": current_url, "daraz_range": daraz_range, "priceOye_range": priceOye_range, "pakmobizone_range": pakmobizone_range})
    except:
        return redirect('Dashboard')
