import requests
import random
import time
from extension import proxies
from selenium import webdriver
from fake_useragent import UserAgent
from babel import Locale
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium_profiles.profiles import profiles
from selenium_profiles.webdriver import Chrome

def get_info():
    user_agent = UserAgent().random
    username = "qk3p77qxjve0cbq-country-us"
    password = "v4gvnuv5zadkk4m"
    host = "rp.proxyscrape.com"
    port = 6060
    proxy = f"{host}:6060"
    proxy_auth = f"{username}:{password}@{proxy}"

    urlToGet = "http://ip-api.com/json"
    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate"
    }
    proxies = {
        "http": f"http://{proxy_auth}",
        "https": f"https://{proxy_auth}"
    }
    response = requests.get(urlToGet, proxies=proxies, headers=headers)
    ip_address = response.json()["query"]
    print(ip_address)
    r = requests.get(f"https://ipapi.co/{ip_address}/json/", headers=headers)
    return r.json()

info = get_info()
proxy_ip, longitude, latitude, timezone, language = info["ip"], info["longitude"], info["latitude"], info["timezone"], info["languages"]
print(proxy_ip, longitude, latitude, timezone, language)
proxies_extension = proxies(username, password, host, port)

def create_stealth_browser(website):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"enable_do_not_track": True})
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument(f'--load-extension={proxies_extension}')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument(f'--user-agent={user_agent}')

    driver = Chrome(profiles.Windows(), options=chrome_options)

    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": latitude, "longitude": longitude, "accuracy": 100})
    driver.execute_cdp_cmd("Emulation.setLocaleOverride", {"locale": language})
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": timezone})

    driver.get(website)
    time.sleep(random.uniform(5, 10))

    print("hello")
    if "Anonymous Proxy detected, click here." in driver.page_source:
        print("Anonymous Proxy detected, click here.")
        time.sleep(1)
        driver.refresh()
        time.sleep(random.uniform(2, 3))
    if driver.current_url == "https://www.google.com/":
        driver.get(website)

    print("Started scrolling...")
    for _ in range(7):
        x, y = random.randint(0, 1920), random.randint(0, 1080)
        driver.execute_script(f"window.scrollTo({x}, {y});")
        time.sleep(random.uniform(1, 2))

    for _ in range(random.randint(2, 7)):
        try:
            driver.find_element(By.TAG_NAME, "a").click()
            time.sleep(random.uniform(1, 2))
            driver.execute_script("window.history.back();")
            time.sleep(random.uniform(1, 2))
            x, y = random.randint(0, 1920), random.randint(0, 1080)
            driver.execute_script(f"window.scrollTo({x}, {y});")
            time.sleep(random.uniform(1, 2))
            print("Successfully Clicked")
        except:
            print("Failed to Click ")
            pass
    
    driver.quit()

if __name__ == "__main__":
    with open("urls.txt", "r") as f:
        websites = [line.strip() for line in f]

    visit_no = 0
    for _ in range(1000):
        for website in websites:
            create_stealth_browser(website)
        visit_no += 1
        print(f"Visited {visit_no} times")
        time.sleep(random.uniform(1, 6))
  
