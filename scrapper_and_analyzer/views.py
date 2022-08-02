from scrapper_and_analyzer.backend.priceoye import priceOye_main
from scrapper_and_analyzer.backend.daraz import daraz_main
from django.shortcuts import redirect, render
import sys
from django.views.decorators.cache import cache_control
sys.path.append('../')

# import daraz.py from python folder
# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):

    return render(request, 'index.html')


def result(request):
    # get browser session storage value

    # get request values
    if request.method == 'POST':

        keyword = request.POST.get('keyword')
        print(keyword)
        if(not bool(keyword)):
            return render(request, 'results.html', context={'msg': "error", "text": "No keyword entered!"})
        else:
            # call scrapper function
            try:

                daraz = daraz_main(keyword)
                priceOye = priceOye_main(keyword)
                if(daraz == None or priceOye == None):
                    return render(request, 'results.html', context={'msg': "error", "text": "No result found!"})
                third_website = {
                    "name": "Demo Product",
                    "price": 10000000000000,
                    "src": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
                }
                # find the lowest price
                price_array = [daraz['price'],
                               priceOye['price'], third_website['price']]
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
                    min_price_product = third_website

                if(highest_index == 0):
                    max_price_product = daraz
                elif(highest_index == 1):
                    max_price_product = priceOye
                else:
                    max_price_product = third_website

                # set values in session
                request.session['daraz'] = daraz
                request.session['priceOye'] = priceOye
                request.session['third_website'] = third_website
                request.session['min_price_product'] = min_price_product
                request.session['max_price_product'] = max_price_product

                return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "third_website": third_website, "min_price_product": min_price_product, "max_price_product": max_price_product})
            except Exception as e:
                return render(request, 'results.html', context={'msg': "error", "text": "Can't find the product or may not exist!"})
    if request.method == 'GET':
        # get values fromm session
        try:
            daraz = request.session['daraz']
            priceOye = request.session['priceOye']
            third_website = request.session['third_website']
            min_price_product = request.session['min_price_product']
            max_price_product = request.session['max_price_product']
            return render(request, 'results.html', context={'msg': "success", 'daraz': daraz, 'priceOye': priceOye, "third_website": third_website, "min_price_product": min_price_product, "max_price_product": max_price_product})
        except:
            return redirect('index')
