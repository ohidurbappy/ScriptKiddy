from googletrans import Translator

translator = Translator()
# use this code for local translator service
# translator = Translator(service_urls=[
#       'translate.google.com',
#       'translate.google.co.kr',
#     ])

# open the file 'google_translate_input.txt' and read line by line
fi=open('google_translate_input.txt','r',encoding='utf-8')
inputList=[line.rstrip('\n') for line in fi]
trans=translator.translate(inputList,dest='bn')

output=''
for tran in trans:
    print(tran.origin+'->'+tran.text)
    output+=tran.origin+'\n:'+tran.text+'\n\n'

f=open('google_translate_output.txt','w',encoding='utf-8')
f.write(output)
f.close()