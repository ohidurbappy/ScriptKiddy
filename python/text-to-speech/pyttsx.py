import pyttsx3
engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate',120)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 0.9)
engine.say("hello crazy programmer")
engine.runAndWait()
