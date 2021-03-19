from gtts import gTTS
import playsound
import os
tts = gTTS(text='আমি ওহিদুর রহমান বাপ্পি । বঙ্গবন্ধু শেখ মুজিবুর রহমান বিজ্ঞান ও প্রযুক্তি বিশ্ববিদ্যালয়ে ইলেক্ট্রিক্যাল এবং ইলেক্ট্রনিক ইঞ্জিনিয়ারিং বিভাগে দ্বিতীয় বর্ষে পড়ি। ', lang='bn')
tts.save("good.mp3")
os.system("mpg321 good.mp3")
playsound.playsound('good.mp3', True)
