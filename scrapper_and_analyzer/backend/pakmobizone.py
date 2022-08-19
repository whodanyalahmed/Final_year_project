
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
import re

from scrapper_and_analyzer.models import Dataset


def Chrome(headless=False):
    # add fake user agent
    chrome_options = webdriver.ChromeOptions()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), options=chrome_options)
    driver.implicitly_wait(5)
    return driver


def minpr(d):
    if d == 0:
        return 100000000000000000000
    else:
        return 1




def pakmobizone_main(keyword, choice):

   
    minprice = minpr(0)
    minname = ""
    mincount = 0

    price_list = []
    title_list = []
    image_list = []
    link_list = []
    keyword_url = keyword.replace(' ', '+')
    driver = Chrome(True)
    driver.implicitly_wait(25)
    url = 'https://www.pakmobizone.pk/?s={}&products=true'.format(keyword_url)
    driver.get(url)
    qt_main = driver.find_element_by_id("qt-main")

    # get div with class qt-phone-thumb

    products = qt_main.find_elements_by_xpath(
        '//div[@class="qt-phone-thumb"]')

    for product in products:
        # get h3 with class qt-phone-thumb-title
        name = product.find_element_by_xpath(
            'h3[@class="qt-phone-thumb-title"]')
        # get div with class qt-phone-thumb-price
        price = product.find_element_by_xpath(
            'div[@class="qt-phone-thumb-price"]').text
        price = str(price).replace('Rs.', '')
        price = price.replace(',', '')
        price = int(price)
        link = product.find_element_by_xpath(
            'a').get_attribute('href')
        image = product.find_element_by_xpath(
            "a/img").get_attribute('src')

        obj, created = Dataset.objects.get_or_create(
            name=name.text, price=price, website="pakmobizone", link=link, image=image)
        fname = name.text.lower()
        keyword_name = keyword.lower().split(' ')
        # get keyword_name except first one
        keyword_name = keyword_name[1:]
        if keyword.lower() in fname or re.search('|'.join(keyword_name), fname):
            price_list.append(price)
            title_list.append(name.text)
            image_list.append(image)
            link_list.append(link)
    dt = dict(zip(title_list, price_list))
    for k, v in dt.items():
        if v < minprice:
            minprice = v
            minname = k

    print("Min. name is : ", minname)
    print("Min. price is : ", minprice)

    # find div with id root
    driver.quit()
    index = price_list.index(minprice)
    if choice == "result":
        return {"price": minprice, "name": minname, "src": image_list[index], "link": link_list[index]}
    else:
        return {"names": title_list, "prices": price_list, "images": image_list, "links": link_list}


if __name__ == '__main__':
    d = pakmobizone_main("Iphone 13")
    print(d)
