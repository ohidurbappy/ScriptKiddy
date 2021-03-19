from PIL import Image, ImageDraw, ImageFont
import textwrap

astr = '''She sells sea shell on the sea shore!'''
para = textwrap.wrap(astr, width=20)

MAX_W, MAX_H = 600, 400
im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('Raleway-bold.ttf', 32)

current_h, pad = 100, 10
for line in para:
    w, h = draw.textsize(line, font=font)
    draw.text(((MAX_W - w) / 2, current_h), line, font=font,fill='red')
    current_h += h + pad

im.save('test.png')