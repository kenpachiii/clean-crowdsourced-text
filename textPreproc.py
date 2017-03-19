#coding: utf-8
"""
A simple script for pre-processing crowdsourced textual data. 
Performs spelling correction in US English (using the word frequency information 
provided by the Brown corpus), expands contractions (e.g. it's to it is), 
translates numbers into words, removes html tags and non-ascii characters.

There are a number of python packages available that would make this task easier 
(e.g. num2words), but clearly it makes more sense to write my own scripts for 
this excercise. 

Author: Nico De Tullio
"""
from txtcleaner import num2words, spell, formatter, tokenizer
from collections import Counter
from nltk.corpus import brown, cmudict
import io

# Import text from Google's 1-Billion Word Benchmark
print "Reading text..."
with io.open('./news-commentary-v6.en', 'r', encoding='utf-8') as fid:
    text = fid.read()
    
# Tokenize 
tokens = tokenizer(text)
                              
print "Convert numbers into words..."
numbers = [str(x) for x in tokens if x.isdigit()]
words = [num2words(num) for num in numbers]
numwords = dict(zip(numbers, words))
tokens_nw = [numwords[x] if x in numwords else x for x in tokens]

#==============================================================================
# Normalise pronunciation to US English and correct misspellings.
# Get the brown and cmudict corpora and count information.
# Will use brown corpus for correction instead of cmudict as the latter 
# does not provide frequency information.
#==============================================================================
print "Load corpora..."
dict_brown = Counter(brown.words())
dict_cmu = Counter(cmudict.words())
# some additional known strings
dict_mine = Counter(["mrs", "miss", "mr", "dr", "prof","dr.","prof.","\n", "lt.",'"'])
full_dict = set(dict_brown+dict_cmu+dict_mine)

print "Correct spelling and US grammar..."
tokens_sp = [x if x in full_dict else spell(x,dict_brown) for x in tokens_nw]
text_sp = ' '.join(word for word in tokens_sp) 
     
# Format text
text_clean = formatter(text_sp)

print "Write cleaned text to 'cleaned_text.txt'..."
with io.open('./cleaned_text.txt', 'w', encoding='utf-8') as fid:
#with open('./cleaned_text.txt', 'w') as fid:
    fid.write(text_clean)

print "Done."


