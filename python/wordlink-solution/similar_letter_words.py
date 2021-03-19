wordlist=[]
mWords=[]

#with open("words2.txt",'r') as file:
#    wordlist=list(line.strip('\n') for line in file)
wordfile=open("words2.txt",'r')
for word in wordfile:
    word=word.strip()
    #if len(word)>=3:
    wordlist.append(word)

for word in wordlist:
    candidate=True
    letterlist=list("hello")
    for letter in word:
        if letter not in letterlist:
            candidate=False
            break
        #else:
        #    letterlist.remove(letter)
        
    if candidate:
        mWords.append(word)
print(mWords)


