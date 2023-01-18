import datetime
import io
import os
import random
import sys
import time
import traceback
from random import shuffle
import pickle

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities, Firefox, FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

if os.name != "nt":
    # os.system("chmod +x geckodriver")
    geckodriver = os.path.abspath("geckodriver")
else:
    geckodriver = os.path.abspath("geckodriver.exe")

# import xvfbwrapper # learn more: https://python.org/pypi/xvfbwrapper

FACEBOOK_LOGIN_PAGE = "https://mbasic.facebook.com"


if __name__ == "__main__":
    try: 
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            "general.useragent.override", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0")
        driver = webdriver.Firefox(
            executable_path=geckodriver,firefox_profile=profile)
        driver.get(FACEBOOK_LOGIN_PAGE)

        email = "whoisohid@gmail.com"
        password = "fedora36"

        time.sleep(1)

        input_email = driver.find_element_by_id('m_login_email')

        input_pass = driver.find_element_by_name('pass')

        input_email.send_keys(email)
        input_pass.send_keys(password)

        login_btn = driver.find_element_by_name('login')

        login_btn.click()

        time.sleep(10)

        # export the cookies
        pickle.dump(driver.get_cookies(),open('cookies.pkl','wb'))

        

        driver.close()

        exit(0)



    except KeyboardInterrupt:
        print("INTERRUPT: Keyboard Interrupt")
        driver.quit()
        os._exit(0)
    except:
        time.sleep(5*60)
    finally:
        driver.quit()
