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


def main():
    driver = Chrome()
    driver.get('https://finviz.com/quote.ashx?t=NANR')
    table = driver.find_elements_by_tag_name("table")[9]
    # print(len(table))
    # get first row
    row1 = table.find_elements_by_tag_name("tr")[0]
    row2 = table.find_elements_by_tag_name("tr")[1]
    row3 = table.find_elements_by_tag_name("tr")[2]
    row4 = table.find_elements_by_tag_name("tr")[3]
    row5 = table.find_elements_by_tag_name("tr")[4]
    row6 = table.find_elements_by_tag_name("tr")[5]
    last_row = table.find_elements_by_tag_name("tr")[-1]
    # get the last two elements
    pref_Week = row1.find_elements_by_tag_name("td")[-1:]
    pref_month = row2.find_elements_by_tag_name("td")[-1:]
    pref_quater = row3.find_elements_by_tag_name("td")[-1:]
    pref_half_year = row4.find_elements_by_tag_name("td")[-1:]
    pref_year = row5.find_elements_by_tag_name("td")[-1:]
    pref_YTD = row6.find_elements_by_tag_name("td")[-1:]
    sma200 = last_row.find_elements_by_tag_name("td")[7:9]
    # print(len(cols))
    # print(len(cols))
    print("pref_week: {}".format(pref_Week[0].text))
    print("pref_month: {}".format(pref_month[0].text))
    print("pref_quater: {}".format(pref_quater[0].text))
    print("pref_half_year: {}".format(pref_half_year[0].text))
    print("pref_year: {}".format(pref_year[0].text))
    print("pref_YTD: {}".format(pref_YTD[0].text))
    print("SMA200: {}".format(sma200[0].text))
    driver.quit()


if __name__ == '__main__':
    main()
