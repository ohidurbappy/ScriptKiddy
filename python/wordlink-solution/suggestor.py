#!python
import re
from collections import Counter
def words(text):
	return re.findall(r'\w+',text.lower())

WORDS=Counter(words(open('words2.txt').read()))

class Suggestor:
	def __init__(self,max_times,letters):
		self.max_times=max_times
		self.letters=letters
	def candidates(self,word):
		return self.known(self.edited_word(word))

	def known(self,words):
		return set(w for w in words if w in WORDS)
	
	def edit(self,word):
		letters=self.letters
		splits=[(word[:i],word[i:]) for i in range(len(word)+2)]
		inserts=[L+C+R for L,R in splits for C in letters]
		return list(set(inserts))
	
	def edited_word(self,raw_word):
		words=[[raw_word]]
		for i in range(self.max_times):
			i_times_words=[]
			for word in words[-1]:
				i_times_words+=self.edit(word)
			words.append(list(set(i_times_words)))
		return [w for word in words for w in word]

if __name__=='__main__':
	word='pny'
	suggestor=Suggestor(max_times=4,letters='aeiou')
	print(suggestor.candidates(word))

