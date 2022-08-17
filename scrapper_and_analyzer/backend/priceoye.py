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


def priceOye_main(keyword, choice):

    minprice = minpr(0)
    minname = ""
    mincount = 0

    price_list = []
    title_list = []
    image_list = []
    link_list = []
    keyword_url = keyword.replace(' ', '+')
    driver = Chrome(True)
    url = 'https://priceoye.pk/search?q=' + keyword_url
    # print(url)
    driver.get(url)
    # product_list = driver.find_element_by_class_name("product-list")
    divs = driver.find_elements_by_xpath(".//div[@class='product-list']/div")
    # print(divs)
    # print(len(divs))
    for div in divs:
        details = div.find_element_by_xpath(".//div[@class='detail-box']")
        name = details.find_element_by_class_name("p3")

        img = div.find_element_by_xpath(
            './/div[@class="image-box desktop"]/amp-img')
        link = div.find_element_by_xpath(
            'a').get_attribute('href')
        # get src attribute of amp-img
        src = img.get_attribute("src")

        # print(src)

        price = details.find_element_by_xpath(".//div[@class='price-box']")
        price = str(price.text)
        price = price.replace("Rs. ", "")
        price = price.replace(",", "")
        price = int(price)

        obj, created = Dataset.objects.get_or_create(
            name=name.text, price=price, website="priceOye", link=link, image=src)
        print("obj and created: ", obj, created)
        fname = name.text.lower()
        keyword_name = keyword.lower().split(' ')
        # get keyword_name except first one
        keyword_name = keyword_name[1:]
        if keyword.lower() in fname or re.search('|'.join(keyword_name), fname):
            title_list.append(name.text)
            image_list.append(src)
            link_list.append(link)
            price_list.append(price)

            print("link: "+link)
            print("name: ", name.text)
            print("price: ", price)
            print("image: ", src)
    dt = dict(zip(title_list, price_list))

    for k, v in dt.items():

        if v < minprice:
            minprice = v
            minname = k

    print("Min. price is : ", str(minprice))

    # return minprice,minname and iamge_link with mincount as index

    driver.quit()

    index = price_list.index(minprice)
    if(choice == "result"):
        return {"price": minprice, "name": minname, "src": image_list[index], "link": link_list[index]}
    else:
        return {"names": title_list, "prices": price_list, "images": image_list, "links": link_list}


if __name__ == '__main__':
    d = priceOye_main("Iphone 11")
    print(d)
