from datetime import datetime
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
from sklearn.ensemble import RandomForestRegressor
from django.db import connection


sys.path.append('../')
# from ..models import Dataset


@register.filter
def index(sequence, position):
    return sequence[position]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def get_predicted_price(request):
    if request.method == 'POST':
        try:
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
            # SELECT *
            # FROM `table`
            # WHERE `column` LIKE '%{$needle}%'
            # trim the data
            formatted_data = str(keyword).strip()
            formatted_keyword = formatted_data.replace(' ', '%')
            formatted_keyword = '%' + formatted_keyword + '%'
            formatted_keyword = formatted_keyword.lower()
            # print(formatted_keyword)
            query = "SELECT * FROM scrapper_and_analyzer_dataset WHERE name like '" + \
                formatted_keyword+"'"

            cursor = connection.cursor()
            data = cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()

            # searialize the data
            print(data)
            # print(data)
            # # get the dataframe
            # get 4 columns name,price,fetched_date
            df = pd.DataFrame(data)
            df.rename(columns={1: 'name', 2: 'price',
                      6: 'fetched_date'}, inplace=True)
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
            X_train, X_test, y_train, y_test = train_test_split(
                x, y, test_size=0.2)
            # reshape new_date to 2d array
            new_date = new_date.values.reshape(-1, 1)
            new_date = [[float(new_date)]]
            print(new_date)
            # model = LinearRegression()
            # model.fit(x, y)
            # r_sq = model.score(x.astype('float64'), y)
            # print(f"coefficient of determination: {r_sq}")
            # print(f"intercept: {model.intercept_}")
            # print(f"slope: {model.coef_}")
            # # y_pred = model.predict(new_date)
            # y_pred = model.predict(new_date)
            # print(f"predicted response:\n{y_pred}")
            # print(f"actual response:\n{y}")
            # y_pred = json.dumps(y_pred, cls=NumpyEncoder)
            clf = LinearRegression(
                copy_X=True, fit_intercept=True, n_jobs=None, normalize=False)
            rf = RandomForestRegressor(n_estimators=1000, random_state=42)
            rf.fit(X_train, y_train)
            clf.fit(X_train, y_train)
            confidence = clf.score(X_test.astype('float64'), y_test)
            print(confidence)
            forecast_set = clf.predict(X_test.astype('float64'))
            rf_set = rf.predict(X_test.astype('float64'))
            print("Actual: %s" % y_test)
            print("Predicted: %s" % forecast_set)
            print("Random Forest Predicted: %s" % rf_set)

            forecast_set = forecast_set.tolist()
            y_pred = clf.predict(new_date)
            rf_y_pre = rf.predict(new_date)
            y_pred = abs(y_pred)
            rf_y_pre = abs(rf_y_pre)
            # round rf_y_pre
            rf_y_pre = np.round(rf_y_pre)
            y_pred = json.dumps(y_pred, cls=NumpyEncoder)
            rf_y_pre = json.dumps(rf_y_pre, cls=NumpyEncoder)
            print("RF: "+rf_y_pre)
            # round the rd_y_pre to 0 decimal places

            # convert y_pred to absolute value

            return rf_y_pre
        except Exception as e:
            print("exception: "+str(e))
            return {"error": "Something went wrong"}


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
            if (current_url != 'list' and current_url != 'prediction'):
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
            elif current_url == "prediction":
                try:
                    data = get_predicted_price(request)

                    print(data)
                    print(type(data))
                    if(isinstance(data, dict)):
                        priceOye_main(keyword, "list")
                        daraz_main(keyword, "list")
                        pakmobizone_main(keyword, "list")

                        data = get_predicted_price(request)
                    # convert to list
                    data = json.loads(data)
                    data = data[0]
                    data = int(data)

                    # save values in session
                    request.session['data'] = data
                    request.session['current_url'] = current_url
                    request.session['keyword'] = keyword
                    return render(request, 'results.html', context={'msg': "success", 'data': data, 'current_url': current_url, 'keyword': keyword})
                except Exception as e:
                    print(e)
                    return render(request, 'results.html', context={'msg': "error", "text": "Can't find the product or may not exist!"})
            else:
                print("in else")
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

        current_url = request.session['current_url']
        try:

            if current_url != 'list' and current_url != 'prediction':
                daraz = request.session['daraz']
                priceOye = request.session['priceOye']
                pakmobizone = request.session['pakmobizone']
                min_price_product, max_price_product = get_min_max_price(
                    daraz, priceOye, pakmobizone)
                return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "pakmobizone": pakmobizone, "min_price_product": min_price_product, "max_price_product": max_price_product, "current_url": current_url})
            elif current_url == "prediction":
                data = request.session['data']
                keyword = request.session['keyword']

                return render(request, 'results.html', context={'msg': "success", 'data': data, 'current_url': current_url, 'keyword': keyword})
            else:
                return redirect('list_result')
        except:
            return redirect('Dashboard')


def list_results(request):
    # get values fromm session
    try:
        print("in list_results")
        daraz = request.session['daraz']
        priceOye = request.session['priceOye']
        pakmobizone = request.session['pakmobizone']
        current_url = request.session['current_url']
        print(daraz)
        print(priceOye)
        print(pakmobizone)
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
    except Exception as e:
        print(e)
        return redirect('Dashboard')
