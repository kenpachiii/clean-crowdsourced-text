#coding: utf-8
"""
A collection of functions that help with the cleaning of crowdsourced textual data.

Author: Nico De Tullio
"""

import re
from contractions import contractions

def num2words(arg):
    """ We will divide the number into 3 digit chunks and process one chunck at a time,
        keeping track of which part of the full number each chunk belongs to. 
        Works with numbers up to hundreds of trillions.""" 
        
    # Numbers dictionaries
    nums = {"1":"one","2":"two","3":"three","4":"four","5":"five","6":"six", "7":"seven","8":"eight","9":"nine"}
    more_nums = {"10":"ten","11":"eleven","12":"twelve","13":"thirteen","14":"fourteen","15":"fifteen","16":"sixteen", "17":"seventeen","18":"eighteen","19":"nineteen"}
    tens = {"2":"twenty","3":"thirty","4":"forty","5":"fifty","6":"sixty", "7":"seventy","8":"eighty","9":"ninety"}
    huge = {0:" trillion, ",1:" billion, ",2:" million, ",3:" thousand, ",4:""}
    
    # Convert three digit numbers into words
    def _digstonum(val):
        res = ""
        if val[0] in nums:
            res = res + nums[val[0]] + " hundred and "
        if val[1:] in more_nums:
            res = res + more_nums[val[1:]] + " "
        elif val[1] in tens:
            res = res + tens[val[1]] + " "
            if val[2] in nums:
                res = res + nums[val[2]]
        elif val[2] in nums:
                res = res + nums[val[2]]
    
        return res
    
    # Get equivalent 15 digit number (fill with zeros)
    nzeros = 15-len(str(arg))
    bignum = "0"*nzeros + str(arg)

    # Get three digit chuncks
    ans =""
    numbers = [bignum[0:3],bignum[3:6],bignum[6:9],bignum[9:12],bignum[12:15]]

    for ind,digs in enumerate(numbers):
        if digs!="000":
            ans = ans + _digstonum(digs) + huge[ind]
                
    return ans
    
def spell(word,dictionary):
    """ For simplicity we will restrict ourselves to mispelled words that are 
        one simple modification away from being written correctly. We will consider
        the following as possible errors: insert one letter, delete one letter,
        change one letter, swap two letters. We will use frequency information 
        from the Brown corpus (i.e. more frequent word = more likely word) 
        to guess the correct spelling."""

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    # Find possible modifications
    inserts = [word[:i]+new+word[i:]    for i in range(len(word)) for new in alphabet]
    deletes = [word[:i]+word[i+1:]  for i in range(len(word))]
    changes = [word[:i]+new+word[i+1:]  for i in range(len(word)) for new in alphabet if new != word[i]]
    swaps   = [(word[:i] + word[j]+word[i+1:j]+word[i]+word[j+1:])  for i in range(len(word)) for j in range(i+1,len(word))]

    mods = set(inserts+deletes+changes+swaps)
    
    # Keep only realistic modifications
    guess = [known for known in mods if known in dictionary]
    guess = (guess or [word]) # return input word if no candidates found    

    return max(guess, key = dictionary.get) # return word with maximum frequency
    
def tokenizer(string):
    """ Tokenize by word, punctuation (including hyphens) and 
        newline character. 
        We will keep the same line format as the input stringfor simplicity. 
        We will to tokenize hypens to spell-check single words in hypenated words.
        Before the above the function will: get rid of html tags, 
        and non-asci characters (\x00-\x7F), remove commas in numbers, and 
        expand contractions using a dictionary extracted from Wikipedia."""

    print "Clean up, expand contractions and tokenize..." 
    # Get rid of HTML tags
    text = re.sub('<[^<]+?>', '', string)
    # Get rid of non-asci
    text_asci = re.sub(r'[^\x00-\x7F]+',' ', text)
    # Get rid of commas in numbers
    text_noc = re.sub(r'[0-9,0-9]([0-9][0-9])',r'\1',text_asci)
    # Unify quotation marks
    text_quot = re.sub('([\']+[\']|[\`]+[\`])', '"', text_noc)
    # Expand contractions
    tokens_exp = [x.lower() if x.lower() not in contractions 
                        else contractions[x.lower()] for x in re.findall(r'\S+|\n',text_quot)]
    text_exp = ' '.join(word for word in tokens_exp) 
    # Tokenize by word and punctuation
    tokens = [x.strip(' ') for x in re.findall(r'\S+|\n | [\w]+|[.,!?;\n] | [(\[{]+|[\w|\n] | [?]',text_exp)]
    # Divide hypenated words
    tokens_nohy = [[x[0],x[1:]] if "-" in x else [x] for x in tokens]  

    # Flatten list and return
    return [item for sublist in tokens_nohy for item in sublist]

def formatter(text):
    """ This takes care of some aesthetics."""
        
    print "Format text..."
    # Strip whitespace before punctuation and apostrophes 
    text_sp = re.sub(r'\s([?.!,:;"](?:\s|$))', r'\1', text)
    text_sp = re.sub(r"\b\s+'\b", r"'", text_sp)
    # and between parentheses
    text_sp = re.sub(r'\s([)\]}](?:\s|$))', r'\1', text_sp)
    text_sp = re.sub(r'((?:\s|$)[(\[{])\s', r'\1', text_sp)
    # and around hypens
    text_sp = re.sub(r'\s(-)\s','-', text_sp)
    # Place space around double hypens
    text_sp = re.sub(r"([a-zA-Z])--", "\\1 --", text_sp)
    text_sp = re.sub(r"--([a-zA-Z])", "-- \\1", text_sp)
    
    # Capitalise first letter of each sentence and lonely i
    clean_text = re.sub('^([a-z])|[\.|\?|\!]\s*([a-z])|\s+([a-z])(?=\.)', lambda x: x.group().upper(), text_sp)
    clean_text = re.sub(r' i ', lambda x: x.group().upper(), clean_text)
    
    # Swap instances of ," to ", and return    
    return re.sub(r'(,")', r'",', clean_text)
    
    
    
    
    
    
    
    
    
    
    