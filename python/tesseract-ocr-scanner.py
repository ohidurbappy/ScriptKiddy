from PIL import Image
import pytesseract

text=pytesseract.image_to_data((Image.open('image.png')))
print(text)
