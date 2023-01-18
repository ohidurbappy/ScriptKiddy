from PIL import Image, ImageFilter,ImageOps
import requests
import os
import json
import traceback

# os.environ["PATH"] += os.pathsep + r"C:\Users\Bappy\AppData\Local\Tesseract-OCR"




OCR_SPACE_API_KEY="6370beda8e88957"
OCR_SPACE_API_ENDPOINT="https://api.ocr.space/parse/image"

def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


def preprocess_captcha(filename):
    threshold1=140
    image=Image.open(filename)
    image.resize(size=(100,28))
    cropped_image=image.crop((0,0,100,17))
    # cropped_image.save('cropped.png')
    gray_scale=cropped_image.convert('L')
    # gray_scale.save('grayscale.png')
    first_threshold=gray_scale.point(lambda p:p>threshold1 and 255)
    # first_threshold.save('t1.png')
    final=first_threshold.filter(ImageFilter.EDGE_ENHANCE)
    final=final.filter(ImageFilter.SHARPEN)
    final.save('final.png')

def get_code():
    path_to_final_image=os.path.join(os.path.dirname(__name__),'final.png')
    preprocess_captcha('captcha.jpg')
    response=json.loads(ocr_space_file(path_to_final_image))

    try:
        captcha_code=response['ParsedResults'][0]['ParsedText']
        captcha_code=str(captcha_code).strip()
        print("Captcha code: ",captcha_code)
        return captcha_code
    except KeyError:
        traceback.print_exc()
        return None
    

if __name__ == "__main__":
    path_to_final_image=os.path.join(os.path.dirname(__name__),'final.png')
    preprocess_captcha('captcha.jpg')
    response=json.loads(ocr_space_file(path_to_final_image))

    try:
        captcha_code=response['ParsedResults'][0]['ParsedText']
        captcha_code=str(captcha_code).strip()
        print("Captcha code: ",captcha_code)
    except KeyError:
        traceback.print_exc()
        