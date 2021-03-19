import re
import itertools

perm=[]
wordlist=[]

for word in itertools.permutations("bangla"):
    perm.append(''.join(word))
    print(''.join(word))

wordfile=open("words.txt","r")
for word in wordfile:
    wordlist.append(word.strip())
    
for w in perm:
    if w in wordlist:
        print(w)
    

print("done")

