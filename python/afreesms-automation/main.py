import urllib
from flask import Flask,request
from flask.helpers import make_response
from selenium import webdriver
from threading import Thread
from selenium.webdriver.common.keys import Keys
from captcha_solver import get_code
from PIL import Image
import requests
import io
import urllib.parse

app=Flask(__name__)

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)


def send_sms(phone,message):
    firefox_profile = webdriver.FirefoxProfile()
    # firefox_profile.set_preference('permissions.default.image', 2)

    firefox_options=webdriver.FirefoxOptions()
    # firefox_options.add_argument('--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1')
    
    # import chromedriver_autoinstaller


    # chromedriver_autoinstaller.install()

    driver=webdriver.Chrome()

    script = 'document.styleSheets[0].insertRule("body{background-image:'' !important;}", 0 )' 

    driver.get("https://www.afreesms.com/intl/bangladesh")

    # driver.execute_script(script)

    driver.implicitly_wait(10)

    driver.find_element_by_id('cookie-site-button-ok').click()

    # save the captcha
    captcha_img=driver.find_element_by_id('captcha')

    img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
          ele.removeEventListener('load', fn, false);
          var cnv = document.createElement('canvas');
          cnv.width = this.width; cnv.height = this.height;
          cnv.getContext('2d').drawImage(this, 0, 0);
          callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, captcha_img)
    
    import base64
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))



    # captcha_img.send_keys(Keys.END)

    # driver.execute_script("document.getElementById('captcha').scrollIntoView();")
    # driver.implicitly_wait(3)
    # captcha_img.save_screenshot('captcha.png')
    # location = captcha_img.location
    # size = captcha_img.size

    # driver.save_screenshot("shot.png")

    # x = location['x']
    # y = location['y']
    # w = size['width']
    # h = size['height']
    # width = x + w
    # height = y + h


    # im = Image.open('shot.png')
    # im = im.crop((int(x), int(y), int(width), int(height)))

    
    # im.save('captcha.png')

    # image_loc=urllib.parse.urljoin("https://afreesms.com/",captcha_img.get_attribute('src'))
    # download_image(image_loc,'captcha.png')
    captcha_code=get_code()
    print(captcha_code)

    # get input element of the code
    captcha_field=driver.find_element_by_xpath('.//*[@id="smsform"]/table/tbody/tr[7]/td[2]/input')

    captcha_field.send_keys(captcha_code)

    phone_num_field=driver.find_element_by_xpath('.//*[@id="smsform"]/table/tbody/tr[4]/td[2]/input[2]')

    phone_num_field.send_keys('1749817193')

    message_field=driver.find_element_by_xpath('.//*[@id="smsform"]/table/tbody/tr[5]/td[2]/textarea')

    message_field.send_keys("Hello buddy what are you doing.?")

    submit_btn=driver.find_element_by_xpath('.//*[@id="smsform"]/table/tbody/tr[9]/td/input[3]')
    
    submit_btn.click()



@app.route('/')
def index():
    phone_number=request.args.get('phone')
    message=request.args.get('message')

    t=Thread(target=send_sms,args=(phone_number,message))
    t.daemon=True
    t.start()

    return make_response({
        'status':100,
        'message':message,
        'phone':phone_number
    })
        

if __name__ == "__main__":
    app.run(debug=True)