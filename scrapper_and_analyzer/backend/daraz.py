from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def Chrome(headless=False):
    # add fake user agent
    chrome_options = Options()

    # return webdriver
    # support to get response status and headers
    d = webdriver.DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'performance': 'ALL'}

    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("user-agent={}".format(
    #     fake_useragent.UserAgent().random))
    # chrome_options.add_experimental_option(
    #     'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--disable-popup-blocking")
    driver = webdriver.Chrome(
        executable_path=r'i://clients//chromedriver.exe', options=chrome_options, desired_capabilities=d)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def minpr(d):
    if d == 0:
        return 100000000000000000000
    else:
        return 1


minprice = minpr(0)
minname = ""
mincount = 0


def daraz_main(keyword):
    global minprice
    global minname
    global mincount
    keyword_url = keyword.replace(' ', '+')
    driver = Chrome(True)
    url = 'https://www.daraz.pk/smartphones/?from=input&q=' + keyword_url

    driver.get(url)
    # find div with id root
    root = driver.find_element_by_id('root')
    # find div with class product-list

    product_div = root.find_element_by_xpath(
        '//div[@data-qa-locator="general-products"]')
    products_card = product_div.find_elements_by_xpath(
        '//div[@class="gridItem--Yd0sa"]')
    print(len(products_card))

    print("="*30)
    product = product_div.find_elements_by_xpath(
        '//div[@class="inner--SODwy"]')
    title = product_div.find_elements_by_xpath(
        '//div[@class="title--wFj93"]')
    price = product_div.find_elements_by_xpath(
        '//div[@class="price--NVB62"]')
    img_Src = product_div.find_elements_by_xpath(
        '//img[@class="image--WOyuZ "]')
    print(len(title))
    print(len(price))
    print(len(img_Src))
    price_list = []
    title_list = []
    image_list = []
    for i in range(len(title)):
        if keyword.lower() in title[i].text.lower():

            print("="*30)

            print(title[i].text)
            title_list.append(title[i].text)
            print(price[i].text)
            int_price = price[i].text.replace('Rs. ', '')
            int_price = int_price.replace(',', '')
            price_list.append(int_price)
            print(img_Src[i].get_attribute('src'))
            image_list.append(img_Src[i].get_attribute('src'))

    # print(product.text)
    print(price_list)
    dt = dict(zip(title_list, price_list))
    print(dt)

    for k, v in dt.items():
        v = int(v.replace(",", ""))

        if v < minprice:
            minprice = v
            minname = k

    print("Min. price is : ", minprice)

    # return minprice,minname and iamge_link with mincount as index

    driver.quit()
    return {"price": minprice, "name": minname, "src": image_list[price_list.index(str(minprice))]}


if __name__ == '__main__':
    d = daraz_main("Iphone 13")
    print(d)
