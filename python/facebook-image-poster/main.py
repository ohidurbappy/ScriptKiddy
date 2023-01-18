import datetime
import io
import logging
import os
import random
import sys
import time
import traceback
from random import shuffle
import pickle

import requests
from PIL import Image
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities, Firefox, FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# from seleniumwire import webdriver


logging.basicConfig(filename="log.txt", format='%(levelname)s: %(asctime)s:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.ERROR)

logger = logging.getLogger()

if os.name != "nt":
    # os.system("chmod +x geckodriver")
    geckodriver = os.path.abspath("geckodriver")
else:
    geckodriver = os.path.abspath("geckodriver.exe")

# import xvfbwrapper # learn more: https://python.org/pypi/xvfbwrapper


FACEBOOK_LOGIN_PAGE = "https://mbasic.facebook.com"


def get_proxy_list():
    proxy_url = "https://www.proxy-list.download/api/v1/get?type=https&country=US"
    response = requests.get(proxy_url)
    if response.status_code != 200:
        return None
    proxies = (response.text.strip()).split("\r\n")
    print(proxies)
    shuffle(proxies)
    return iter(proxies)


def download_image(url, image_file_path):
    try:
        r = requests.get(url, timeout=10.0)
        if r.status_code != requests.codes.ok:
            # assert False, 'Status code error: {}.'.format(r.status_code)
            return False

        with Image.open(io.BytesIO(r.content)) as im:
            im.save(image_file_path)
            return True
    except:
        return False
    return False


def get_proxy(session, proxies, validated=False):
    session.proxies = {'https': 'https://{}'.format(next(proxies))}
    print(session.proxies)
    if validated:
        while True:
            try:
                return session.get('https://httpbin.org/ip').json()
            except Exception:
                session.proxies = {'https': 'https://{}'.format(next(proxies))}


def get_working_proxy():
    session = requests.Session()
    proxies = get_manual_proxies_iter()

    response = get_proxy(session, proxies, validated=True)
    t = response['origin']

    px = get_manual_proxies()

    for p in px:
        if t in p:
            return p


def get_manual_proxies():
    return [line.rstrip('\n') for line in open("proxies.txt")]


def get_manual_proxies_iter():
    proxies = list(get_manual_proxies())
    shuffle(proxies)
    return iter(proxies)


def get_response(url):
    session = requests.Session()
    proxies = get_manual_proxies_iter()
    while True:
        try:
            # collect a working proxy to be used to fetch a valid response
            print(get_proxy(session, proxies, validated=True))
            # as soon as it fetches a valid response, it will break out of the while loop
            return session.get(url)
        except StopIteration:
            raise  # No more proxies left to try
        except Exception:
            pass  # Other errors: try again


if __name__ == "__main__":
    # start display
    if os.name != 'nt':
        display = Display(visible=0, size=(1920, 600))
        display.start()

    while True:
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            "general.useragent.override", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
        driver = webdriver.Firefox(
            executable_path=geckodriver, firefox_profile=profile)

        # load the cookies
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        for cookie in cookies:
            driver.add_cookie(cookie)

        while True:
            try:
                print("Getting Working proxy...")
                # working_proxy = get_working_proxy()
                print("Downloading photo...")
                if download_image("https://www.ohidur.com/memes/random.jpg", "photo.jpg") == False:
                    continue

                #binary = FirefoxBinary('/home/pi/firefox/firefox')

                # proxy
                # http=working_proxy.replace("https","http")
                # options = {'proxy': {'http': http,
                #                      'https': working_proxy,
                #                       'no_proxy': ''}}

                driver.get(FACEBOOK_LOGIN_PAGE)

                # tw = driver.execute_script("return document.body.offsetWidth") #get total width
                # th = driver.execute_script("return document.body.parentNode.scrollHeight") #get total height
                # driver.set_window_size(tw, th)
                # time.sleep(10) # wait for the page to fully load
                # now = datetime.datetime.now()
                # fn = 'msh_{}.{:0>2}.{:0>2}-{:0>2}.{:0>2}.{:0>2}.png'.format(now.year, now.month, now.day, now.hour, now.minute, now.second) #file name with datestamp
                # screenshot = driver.save_screenshot('{}'.format(fn))
                # print("Process complete!\nGenerated file: '{}'".format(pathwb, fn))
                # driver.set_window_size(800, 600)

                driver.get('https://mbasic.facebook.com/composer/mbasic/?c_src=page_self&referrer=pages_feed&target=170763326830717&ctype=inline&cwevent=composer_entry&icv=lgc_view_photo&lgc_view_photo&av=170763326830717')

                file_upload = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.NAME, "file1"))
                )

                filename = os.path.abspath("photo.jpg")
                file_upload.send_keys(filename)
                file_upload.submit()

                print("Successfully Posted")
                print("Waiting for 25 minute..")
                time.sleep(25*60)

            except KeyboardInterrupt:
                print("INTERRUPT: Keyboard Interrupt")
                driver.close()
                os._exit(0)
            except:
                traceback.print_exc()
                logger.error("An Exception occured")
                time.sleep(5*60)