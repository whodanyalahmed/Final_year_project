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
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
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


def priceOye_main(keyword):
    global minprice
    global minname
    global mincount
    price_list = []
    title_list = []
    image_list = []
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

        img = div.find_element_by_xpath(
            './/div[@class="image-box desktop"]/amp-img')
        # get src attribute of amp-img
        src = img.get_attribute("src")
        image_list.append(src)
        # print(src)
        details = div.find_element_by_xpath(".//div[@class='detail-box']")
        name = details.find_element_by_class_name("p3")
        title_list.append(name.text)
        price = details.find_element_by_xpath(".//div[@class='price-box']")
        price = str(price.text)
        price = price.replace("Rs. ", "")
        price = price.replace(",", "")
        price_list.append(price)

        print("name: ", name.text)
        print("price: ", price)
        print("image: ", src)
    dt = dict(zip(title_list, price_list))

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
    d = priceOye_main("Iphone 11")
    print(d)
