import nltk
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize, punkt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import itertools
import glob
import re
import os
from helper import *
from invertedIndex import *
from preprocessing import *
Stopwords = set(stopwords.words('english'))
ps = PorterStemmer()

unique_words_all = []
unique_words_all_un = []
file_folder = os.getcwd()
file_folder += '/dataset'
inverted_index = {}
files_with_index = {}
linked_list_data = {}

# main query

findAllUniqueWords(unique_words_all, unique_words_all_un, file_folder, files_with_index, Stopwords, ps)
initialiseInvertedIndex(unique_words_all, linked_list_data, files_with_index, Stopwords, ps)
invertedIndexForPermutations(inverted_index, files_with_index, Stopwords, ps)

query = input('Enter your query:')
query = query.lower()
query = word_tokenize(query)
query_spellings = query.copy()
query = [ps.stem(word) for word in query]
connecting_words = []
cnt = 1
different_words = []
different_words_spellings = []
for word in query:
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        different_words.append(word.lower())
    else:
        connecting_words.append(word.lower())

for word in query_spellings:
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        different_words_spellings.append(word.lower())
    else:
        pass

perms_dict = dict()
perms_dict_spellings = dict()
for i,word in enumerate(different_words):

  if contains_star(word):
    perms_dict[word] = permuterm(word)

for i,word in enumerate(different_words_spellings):

  if contains_star(word):
    perms_dict_spellings[word] = permuterm(word)




print(unique_words_all[:10])
print(unique_words_all_un[:10])



for i, word in enumerate(different_words_spellings):
  if word not in perms_dict_spellings.keys():
  
    if unique_words_all_un.count(word) == 0:
      spelling_score = dict()
      for word_1 in unique_words_all_un:
        score=edit_distance(word,word_1)
        spelling_score[word_1]=score

      spelling_score = dict(sorted(spelling_score.items(), key = lambda x: x[1]))
      new_word = list(spelling_score.keys())
      different_words[i]=ps.stem(new_word[0])






# print(different_words)
final_docs = set()
queries_to_be_passed = list()

for i,v in enumerate(different_words):
  if v in perms_dict.keys():
    print(perms_dict[v])
    pass
  else:
    perms_dict[v]=[v]


args = list()

for v in different_words:
  args.append(perms_dict[v])
  print(perms_dict[v])
  



print("**********")
for combination in itertools.product(*args):
  query = list(combination)
  output = set(documents(query, connecting_words))
  final_docs = final_docs.union(output)


print(final_docs)
