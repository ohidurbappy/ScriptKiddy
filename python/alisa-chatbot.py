import pyttsx3
import speech_recognition
import datetime
import wikipedia
import webbrowser
import os
import time
import requests
from bs4 import BeautifulSoup
import re
import random
import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
from googletrans import Translator

translator = Translator(service_urls=['translate.google.com','translate.google.co.ee',])

b="Alisa: "
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main1():
    h=int(datetime.datetime.now().hour)
    if h>8 and h<12:
        print(b,'Good Morning. My name is Alisa. Version 1.02')
        speak('Good morning. My name is Alisa. Version 1.02')
    elif h>=12 and h<17:
        print(b,"Good afternoon. My name is Alisa. Version 1.02")
        speak('Good afternoon. My name is Alisa. Version 1.02')
    else:
        print(b,'Good evening! My name is Alisa. Version 1.02')
        speak('Good evening My name is Alisa. Version 1.02')
    print(b,'How can I help you, Nijat?')
    speak('How can I help you, Nijat?')
motiv="Sometimes later becomes never. Do it now. Nijat, I believe you, you have made me."
need_list=['Nijat, what can I do for you?', 'Do you want something else?', 'Nijat, give me questions or tasks', 'I want to take time with you, do you want to know something else?','Nijat, what is on your mind?', 'I can not think like you-humans, but can give answer your all questions',"Let's discover this world! What do you want to learn today?" ]
sorry_list=['Nijat, I am sorry I dont know how can I say answer', 'I dont have an idea about it, Nijat','Sorry, Nijat! try again']
bye_list=['Good bye, Nijat. I will miss you','See you Nijat','Bye, dont forget I will always be here']
comic_list=['It is not a comic, Nijat. I was serious','Do you think that you are comic? SHUT UP!']
greet_list=['Hi Nijat', 'Hi my dear']
def weather():
    weather_url="https://www.meteoblue.com/en/weather/week/tartu_estonia_588335"
    page3=requests.get(weather_url)
    
    soup=BeautifulSoup(page3.content, "html.parser")
    name = soup.find("div",{"class":"temps"}).text.replace("\n","").strip()
    name2= soup.find("div",{"class":"wind"}).text.replace("\n","").strip()
    name=re.search(r'\d+',name).group()
    print('Currently, temperature is '+name+ ' degree in Tartu. Besides of this, wind speed is '+name2+'. Source: '+weather_url)
    speak ('Currently, temperature is '+name+ ' degree in Tartu. Besides of this, wind speed is '+name2+'. Please click the source for sure.')

def calendarr():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'credentials.json'
    APPLICATION_NAME = 'Google Calendar - Raw Python'
     
     
    def get_credentials():
        """Gets valid user credentials from storage.
     
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
     
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'credentials.json')
     
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
     
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)   
    
    result= service.calendarList().list().execute()
    calendar_id=result['items'][0]['id']
    start_date = datetime.datetime.today().isoformat() + 'Z'
    end_date = datetime.date.today() + datetime.timedelta(days=1)
    
    result=service.events().list(calendarId=calendar_id,timeZone='Europe/Tallinn').execute()
    
    tomorrow=datetime.date.today() + datetime.timedelta(days=1)
    to=tomorrow.strftime("%Y-%m-%d")
    a=input()
    count=[]
    for i in range(0, len(result['items'])):
        if a=='tomorrow lecture':
            x=to+result['items'][i]['start']['dateTime'][10:]
            if x in result['items'][i]['start']['dateTime']:
                count.append(result['items'][i])
    
    if len(count)>0:
        print('You have '+str(len(count))+' lectures for tomorrow.')
        for i in range(0, len(count)):
            s = translator.translate(count[0]['summary'], dest='en',src='et')
            print(s.text + '  will start at '+count[i]['start']['dateTime'][11:16] +'. Lecture will finish at '+count[i]['end']['dateTime'][11:16]+'. The adress is '+count[i]['location']+ ' and your teacher will be '+count[i]['description'])

def takeCommand():
    while True:
        print(" ")
        query=input("Nijat: ")
        if 'who is' in query.lower():
            try:
                query=query.replace('who is','')
                result=wikipedia.summary(query, sentences=2)
                print(b,result)
                speak(result)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
        elif 'hello'==query:
            greet=random.choice(greet_list)
            print(b, greet)
            speak(greet)
            
        elif 'play' in query.lower():
            query=query.replace('play','')
            url='https://www.youtube.com/results?search_query='+query
            webbrowser.open(url)
            time.sleep(2)
            speak('There are a lot of music, select one.')
            time.sleep(3)
            need=random.choice(need_list)
            print(b, need)
            speak(need)
        elif query=='exit' or query=="bye":
            bye=random.choice(bye_list)
            print(b, bye)
            speak(bye)
            break
        elif 'haha' in query:
            comic=random.choice(comic_list)
            print(b, comic)
            speak(comic)
        elif 'motivate' in query:
            print(b, motiv)
            speak(motiv)
        elif 'facebook' in query:
            url2='https://www.facebook.com/friends/requests/?fcref=jwl'
            webbrowser.open(url2)
        elif "current weather"==query:
            weather()
            need=random.choice(need_list)
            print(b, need)
            speak(need)
        elif 'shutdown laptop' in query.lower():
            os.system("shutdown /s /t 1");
        elif "when" or "how" or "who" in query:
            query=query.replace(' ','+')
            page2=requests.get("https://answers.search.yahoo.com/search;_ylt=AwrC1Ch4XUVeKGwAkzhPmolQ;_ylc=X1MDMTM1MTE5NTIxNQRfcgMyBGZyAwRncHJpZAMxMmF3YVpRQlRWU1ZnM2NXNE5QRVhBBG5fcnNsdAMwBG5fc3VnZwM0BG9yaWdpbgNhbnN3ZXJzLnNlYXJjaC55YWhvby5jb20EcG9zAzIEcHFzdHIDaG93JTIwY2FuJTIweW91JTIwcHJvdGVjdARwcXN0cmwDMTkEcXN0cmwDMzMEcXVlcnkDaG93JTIwY2FuJTIweW91JTIwcHJvdGVjdCUyMHdhdGVyBHRfc3RtcAMxNTgxNjA0MjQ5?p="+query+"&fr2=sa-gp-answers.search&guce_referrer=aHR0cHM6Ly9hbnN3ZXJzLnNlYXJjaC55YWhvby5jb20v&guce_referrer_sig=AQAAACHN4HuxaFHfJJH6Sl36bkFJRRn_BEdTtmdtgRqgZq5L36SsFqMIoPtOFssoaRlg1b_a3JZdK4X1UrcbTau9cYHNOH7O7m9dtqZnZfd6fe8PpjsuUZ6kuL5fIx8FaE4tpOKWEjAojxs_-bl6aA8v3oy2FNXJnxwbBTOaiRe3RteE&_guc_consent_skip=1581604327")
            
            soup=BeautifulSoup(page2.content, "html.parser")
            
            name = soup.find("div",{"class":"dd algo fst AnswrsV2"})
            try:
                for link in name.findAll('a', attrs={'href': re.compile("^https://answers.yahoo.com/question")}):
                    a= (link.get('href'))
                    
                page1=requests.get(a)
                
                soup=BeautifulSoup(page1.content, "html.parser")
                
                name = soup.find("div",{"class":"AnswersList__container___3vQdv"}).text.replace("\n","").strip()
                temp=name.rsplit("Favorite Answer",1)
                temp=temp[1].split('.')
                
                for i in temp[:2]:
                    print(b, i)
                    speak(i)
                need=random.choice(need_list)
                print(b, need)
                speak(need)
            except Exception as e:
                sorry=random.choice(sorry_list)
                print(b, sorry)
                speak(sorry)
        
time.sleep(2)
print('Initializing...')
time.sleep(2)
print('Alisa is preparing...')
time.sleep(2)
print('Environment is building...')
time.sleep(2)
main1()
takeCommand()
  
