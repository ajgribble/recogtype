# ----------------------------------------------------------------------------
# --- Author:   Adam Gribble                                               ---
# --- Title:    char_chain_counter.py                                      ---
# --- Date:     July 13, 2012                                              ---
# --- Summary:  Python script for counting character chains in text. Helps ---
# ---           in deciding if a piece of text has enough useful keystrokes---
import os

class CharacterChainCounter():
    def __init__(self):         
        self.chain_count = {}
        self.total = {}
        self.encountered = {}       
        
        # Initialize variables to store character chain counts
        self.chain_count['first'] = 0
        self.chain_count['second'] = 0
        self.chain_count['third'] = 0
        self.chain_count['last'] = 0
        self.chain_count['digraph'] = 0
        self.chain_count['trigraph'] = 0
        self.chain_count['double'] = 0
        self.chain_count['l2'] = 0
        self.chain_count['l3'] = 0
        self.chain_count['l4'] = 0
        self.chain_count['ln'] = 0

        # Initializes possibles character chains
        self.total['first'] = 0
        self.total['second'] = 0
        self.total['third'] = 0
        self.total['last'] = 0
        self.total['digraph'] = 0
        self.total['trigraph'] = 0
        self.total['double'] = 0
        self.total['l2'] = 0
        self.total['l3'] = 0
        self.total['l4'] = 0
        self.total['ln'] = 0

        # Initializes encountered character chain lists
        self.encountered['first'] = {}
        self.encountered['second'] = {}
        self.encountered['third'] = {}
        self.encountered['last'] = {}
        self.encountered['digraph'] = {}
        self.encountered['trigraph'] = {}
        self.encountered['double'] = {}
        self.encountered['l2'] = {}
        self.encountered['l3'] = {}
        self.encountered['l4'] = {}
        self.encountered['ln'] = {}

    def check_first_letter(self, word):
        # The most common first letter in a word in order of frequency
        first_letters = ['t','o','a','w','b','c','d','s','f', 
                         'm','r','h','i','y','e','g','l','n', 
                         'u','j','k']
        
        # Check if the word starts with any of the common letters
        for i in first_letters:
            if i == word[0].lower():
                self.chain_count['first'] += 1
                if i not in self.encountered['first']:
                    self.encountered['first'][i] = 1
                else:
                    self.encountered['first'][i] += 1
                return self.chain_count['first']

    def check_second_letter(self, word):
        # The most common second letter in a word in order of frequency
        second_letters = ['h','o','e','i','a','u','n','r','t']

        if len(word) > 1:
        # Check if the words' second letter is common
            for i in second_letters:
                if i == word[1].lower():
                    self.chain_count['second'] += 1
                    if i not in self.encountered['second']:
                        self.encountered['second'][i] = 1
                    else:
                        self.encountered['second'][i] += 1
                        return self.chain_count['second']
        else:
            return self.chain_count['second']

    def check_third_letter(self, word):
        # The most common third letter in a word in order of frequency
        third_letters = ['e','s','a','r','n','i']
        
        if len(word) > 2:
            # Check if the words' third letter is common
            for i in third_letters:
                if i == word[2].lower():
                    self.chain_count['third'] += 1
                    if i not in self.encountered['third']:
                        self.encountered['third'][i] = 1
                    else:
                        self.encountered['third'][i] += 1
                    return self.chain_count['third']
        else:
            return self.chain_count['third']

    def check_end_letter(self, word):
        # More than half of all words end with
        ending_letters = ['e','t','d','s']
        
        # Check if the words' last letter is common
        for i in ending_letters:
            if i == word[-1]:
                self.chain_count['last'] += 1
                if i not in self.encountered['last']:
                    self.encountered['last'][i] = 1
                else:
                    self.encountered['last'][i] += 1
                return self.chain_count['last']

    def check_digraphs(self, word):
        # Most common digraphs on order of frequency
        common_digraphs = ['th','he','an','in','er','on','re','ed','nd', 
                       'ha','at','en','es','of','nt','ea','ti','to', 
                       'io','le','is','ou','ar','as','de','rt','ve']
        
        # Check if the word contains the digraph
        for j, ue in enumerate(word):
            try:
                digraph = word[j]+ word[j+1]
            except:
                continue
            if digraph.lower() in common_digraphs:
                self.chain_count['digraph'] += 1
                if j not in self.encountered['digraph']:
                    self.encountered['digraph'][digraph] = 1
                else:
                    self.encountered['digraph'][digraph] += 1

    def check_trigraphs(self, word):
        # The most common trigraphs in order of frequency
        common_trigraphs = ['the','and','tha','ent','ion','tio','for','nde', 
                        'has','nce','tis','oft','men']

        # Check if the word contains the trigraph
        for j, ue in enumerate(word):
            try:
                trigraph = word[j] + word[j+1] + word[j+2]
            except:
                continue
            if trigraph.lower() in common_trigraphs:
                self.chain_count['trigraph'] += 1
                if j not in self.encountered['trigraph']:
                    self.encountered['trigraph'][trigraph] = 1
                else:
                    self.encountered['digraph'][trigraph] += 1

    def check_doubles(self, word):
        # The most common double letters in order of frequency
        common_doubles = ['ss','ee','tt','ff','ll','mm','oo']

        # Check if the word contains the double
        for i, val in enumerate(common_doubles):
            for j, ue in enumerate(word):
                try:
                    double = word[j]+ word[j+1]
                except:
                    continue
                if val == double:
                    self.chain_count['double'] += 1
                    if i not in self.encountered['double']:
                        self.encountered['double'][double] = 1
                    else:
                        self.encountered['double'][double] += 1

    def check_l2_words(self, word):
        # The most common two-letter words in order of frequency
        common_l2_words = ['of','to','in','it','is','be','as','at','so', 
                       'we','he','by','or','on','do','if','me','my', 
                       'up','an','go','no','us','am'] 

        if word in common_l2_words:
            self.chain_count['l2'] += 1
            if word not in self.encountered['l2']:
                self.encountered['l2'][word] = 1
            else:
                self.encountered['l2'][word] += 1
            return self.chain_count['l2']

    def check_l3_words(self, word):
        # The most common three-letter words in order of frequency
        common_l3_words = ['the','and','for','are','but','not','you', 
                       'all','any','can','had','her','was','one', 
                       'our','out','day','get','has','him','his', 
                       'how','man','new','now','old','see','two', 
                       'way','who','boy','did','its','let','put', 
                       'say','she','too','use'] 

        if word in common_l3_words:
            self.chain_count['l3'] += 1
            if word not in self.encountered['l3']:
                self.encountered['l3'][word] = 1
            else:
                self.encountered['l3'][word] += 1
            return self.chain_count['l3']

    def check_l4_words(self, word):
        # The most common four-letter words in order of frequency
        common_l4_words = ['that','with','have','this','will','your', 
                       'from','they','know','want','been','good', 
                       'much','some','time','very','when','come', 
                       'here','just','like','long','make','many', 
                       'more','only','over','such','take','than', 
                       'them','well','were'] 

        if word in common_l4_words:
            self.chain_count['l4'] += 1
            if word not in self.encountered['l4']:
                self.encountered['l4'][word] = 1
            else:
                self.encountered['l4'][word] += 1
            return self.chain_count['l4']

    def check_ln_words(self, word):
        # The most commonly used words in the English language 
        # in order of frequency
        most_common_words =['the','of','and','to','in','a','is','that',
                        'be','it','by','are','for','was','as','he',
                        'with','on','his','at','which','but','from',
                        'has','this','will','one','have','not','were',
                        'or','all','their','an','I','there','been',
                        'many','more','so','when','had','may','today',
                        'who','would','time','we','about','after',
                        'dollars','if','my','other','some','them',
                        'being','its','no','only','over','very','you',
                        'into','most','than','they','day','even',
                        'made','out','first','great','must','these',
                        'can','days','every','found','general','her',
                        'here','last','new','now','people','public',
                        'said','since','still','such','through',
                        'under','up','war','well','where','while',
                        'years','before','between','country','debts',
                        'good','him','interest','large','like','make',
                        'our','take','upon','what'] 

        if word in most_common_words:
            self.chain_count['ln'] += 1
            if word not in self.encountered['ln']:
                self.encountered['ln'][word] = 1
            else:
                self.encountered['ln'][word] += 1
            return self.chain_count['ln']

    def check_possible_count(self, words):
        for word in words:
            length = len(word)
            if length > 2:
                self.total['third'] += 1
                
                trigraphs = len(word) - 2
                self.total['trigraph'] += trigraphs
            
            if length > 1:
                self.total['second'] += 1
                for n, letter in enumerate(word):
                    try:
                        if letter == word[n + 1]:
                            self.total['double'] += 1
                    except:
                        continue
                digraphs = len(word) - 1
                self.total['digraph'] += digraphs
            
            if length == 2:
                self.total['l2'] += 1
            elif length == 3:
                self.total['l3'] += 1
            elif length == 4:
                self.total['l4'] += 1
            else:
                continue

        self.total['first'] = len(words)
        self.total['last'] = len(words)
        self.total['ln'] = len(words)

# Opens file from local text folder using the file name from the user's input
file_name = raw_input("Enter the name of the text file: ")
file_path = "text_files/" + file_name + ".txt"
f = open(file_path, "r")

# Reads in text
raw_data = f.read()

# Remove new lines
raw_data = raw_data.replace("\n", "")

# Splits data up into words
split_data = raw_data.split(' ')

# Remove special chars from words
words = []
for word_ in split_data:
    words.append(''.join(char for char in word_ if char.isalnum()))

# Create a new character chain counter
ccc = CharacterChainCounter()

ccc.check_possible_count(words)

for word in words:
    ccc.check_first_letter(word)
    ccc.check_second_letter(word)
    ccc.check_third_letter(word)
    ccc.check_end_letter(word)
    ccc.check_digraphs(word)
    ccc.check_trigraphs(word)
    ccc.check_doubles(word)
    ccc.check_l2_words(word)
    ccc.check_l3_words(word)
    ccc.check_l4_words(word)
    ccc.check_ln_words(word)
    
# Output results
for key, val in ccc.chain_count.items():
    print str(key).title() + " Letter Count: " + str(val) + \
      " out of possible " + str(ccc.total[key])

print "\n------------------------------\n"

for key, val in ccc.encountered.items():
    for k, v in val.items():
        print key.title() + " Character Chain: " + k + " encountered " + str(v) \
              + " times."
#        print k, v

# Closes the file
f.close()

