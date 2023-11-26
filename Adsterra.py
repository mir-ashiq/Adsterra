
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

profile = profiles.Windows() # or .Android
user_agent = UserAgent().random

username = "qk3p77qxjve0cbq-country-us"
password = "v4gvnuv5zadkk4m"
host = "rp.proxyscrape.com"
port = 6060
proxy = f"{host}:6060"
proxy_auth = "{}:{}@{}".format(username, password, proxy)

def get_info():
    urlToGet = "http://ip-api.com/json" #"http://ipapi.co/json"
    headers = {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate"}
    proxies = {
    "http":"http://{}".format(proxy_auth),
    "https":"https://{}".format(proxy_auth)
}
    urlToGet = "http://ip-api.com/json"
    response = requests.get(urlToGet , proxies=proxies, headers=headers)
    ip_address = response.json()["query"]
    print(ip_address)
    r = requests.get(f"https://ipapi.co/{ip_address}/json/", headers=headers)
    return r.json()
    # else:
    #     print(response.status_code)
    #     print("error")
    #     return None

info = get_info()
#print(info)
proxy_ip = info["ip"]
longitude = info["longitude"]
latitude = info["latitude"]
timezone = info["timezone"]
language = info["languages"]
print(proxy_ip, longitude, latitude, timezone, language )
proxies_extension = proxies(username, password, host, port)



def stealth_browser(website):
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {"enable_do_not_track": True})
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_extension(proxies_extension)
    #chrome_options.add_experimental_option("detach", True)

    # Disable automation script (only required when not using the actual headless browser)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'--user-agent={user_agent}')
    # Set DNS same as proxy IP
    #chrome_options.add_argument(f'--host-resolver-rules="MAP * {proxy_ip}"')

    # Instantiate the webdriver
    driver = Chrome(profile, options=chrome_options)

    # Align the browser's location, language, and timezone with the proxy IP
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {"latitude": latitude, "longitude": longitude, "accuracy": 100})
    driver.execute_cdp_cmd("Emulation.setLocaleOverride", {"locale": language})
    driver.execute_cdp_cmd("Emulation.setTimezoneOverride", {"timezoneId": timezone})

    # Navigate to the specified website
    driver.get(website)
    #time.sleep(1000)
    time.sleep(random.uniform(5, 10)) # Pause briefly
    
    print("hello")
    if "Anonymous Proxy detected, click here." in driver.page_source: #== driver.find_element(By.TAG_NAME,"body"):
        print("Anonymous Proxy detected, click here.")
        time.sleep(1)
        driver.refresh()
        time.sleep(random.uniform(2, 3))
    if driver.current_url == "https://www.google.com/":
        driver.get(website)

    # Simulate random clicks, and fluidly scroll up and down for 30-40 seconds 
    print("Started scrolling...")

    for _ in range(7):
        x, y = random.randint(0, 1920), random.randint(0, 1080)
        driver.execute_script("window.scrollTo({}, {});".format(x, y))
        time.sleep(random.uniform(1, 2))

    # # Select any URL, spend 20-40 seconds on the destination website, return to the previous page, and engage in random scrolling for 20-30 seconds

    for _ in range(random.randint(2, 7)):
        try:
            driver.find_element(By.TAG_NAME, "a").click()
            time.sleep(random.uniform(1, 2))
            driver.execute_script("window.history.back();")
            time.sleep(random.uniform(1, 2))
            x, y = random.randint(0, 1920), random.randint(0, 1080)
            driver.execute_script("window.scrollTo({}, {});".format(x, y))
            time.sleep(random.uniform(1, 2))
            print("Successfully Clicked")
        except:
            print("Failed to Click ")
            pass
    
    #Gracefully close the browser
    driver.quit()

if __name__ == "__main__":
    with open("urls.txt", "r") as f:
        websites = f.readlines()
        
    visit_no = 0
    for _ in range(1000):
        for website in websites:
         website = random.choice(websites).strip()  # strip to remove newline characters
         stealth_browser(website)
        visit_no += 1
        print(f"Visited {visit_no} times")
        time.sleep(random.uniform(1, 6))  # add a delay between opening different websites
