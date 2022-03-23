import glob
import os
from helper import *
from invertedIndex import *
from nltk.tokenize import sent_tokenize , word_tokenize, punkt



def findAllUniqueWords(unique_words_all, unique_words_all_un, file_folder, files_with_index, Stopwords, ps):
  '''Find all the unique words in the entire dataset of documents
     before and after performing stemming.

     Parameters:
          **unique_words_all** ( *list* ): List containing stemmed unique words and their frequencies

          **unique_words_all_un** ( *list* ): List containing unstemmed unique words and their frequencies

          **file_folder** ( *str* ): The path to the dataset

          **files_with_index** ( *dict* ) : Dictionary to associate filenames to a unique numeric index

          **Stopwords** ( *set* ): Set of stopwords

          **ps** ( *PorterStemmer object* ): Class object which performs stemming
    

     After the execution of the function, **unique_words_all** and 
     **unique_words_all_un** will be altered for future
     preprocessing.
     '''
  dict_global = {}
  dict_global_un = {}   # dict_global dictionary 
  idx = 1   # number the documents starting from 1
  for file in glob.iglob(f'{file_folder}/*'):
      # print(file)
      fname = file
      file = open(file , "r")                  # Open and
      text = file.read()                       # read file
      text = remove_special_characters(text)   # Remove special characters
      text = re.sub(re.compile('\d'),'',text)  # Remove digits from text
      words = word_tokenize(text)              # Tokenized 'words' array
      words = [word for word in words if len(words)>1]  # Remove words with length = 1
      words = [word.lower() for word in words]          # Convert word to lowercase
      words = [word for word in words if word not in Stopwords]  # Remove stopwords
      temp = words
      words = [ps.stem(word) for word in words]                  # Stemming 
      # words = [word.lower() for word in words]                  
      dict_global.update(finding_all_unique_words_and_freq(words))  # Update global dictionary
      dict_global_un.update(finding_all_unique_words_and_freq(temp))
      files_with_index[idx] = file_folder + '/'
      files_with_index[idx] = files_with_index[idx] + os.path.basename(fname)              # Put file into files_with_index array
      idx = idx + 1                                                # and update index
  unique_words_all_un = list(set(dict_global_un.keys())) 
  unique_words_all = list(set(dict_global.keys()))  








def initialiseInvertedIndex(unique_words_all, linked_list_data, files_with_index, Stopwords, ps):
  '''Initialise the inverted index data structure for all the words.

     Parameters:
          **unique_words_all** ( *list* ): List containing the set of all unique words.

          **linked_list_data** ( *dict* ): Dictionary with the word as key and its inverted index list as the value.

          **files_with_index** ( *dict* ): Dictionary with a numeric index as key and filename as value.

          **Stopwords** ( *set* ): Set of all stopwords.

          **ps** ( *PorterStemmer object* ): Class object which performs stemming.
      
      After the execution of the function, **linked_list_data** will contain the inverted index
      for each unique word in the dataset
  '''
  for word in unique_words_all:                      # For each word,
      linked_list_data[word] = SlinkedList()         # create head
      linked_list_data[word].head = Node(1,Node)     # and head is pointing to a dummy node
  word_freq_in_doc = {}                              # Word freq in a particular document
  for idx, file in files_with_index.items():                  # For each file,
    file = open(file, "r")                         # open
    text = file.read()                             # read
    text = remove_special_characters(text)         # remove spc char
    text = re.sub(re.compile('\d'),'',text)        # remove digits
    words = word_tokenize(text)                    # return list of words
    words = [word for word in words if len(words)>1] # remove words of len 1
    words = [word.lower() for word in words]         # convert words to lowercase
    words = [word for word in words if word not in Stopwords] # remove stopwords
    words = [ps.stem(word) for word in words]             # stemming            
    word_freq_in_doc = finding_all_unique_words_and_freq(words) # Find word freq in a particular file
    for word in word_freq_in_doc.keys():                        # Populate word_freq_in_doc
      linked_list = linked_list_data[word].head               # Get head of inverted index of that word
      while linked_list.nextval is not None:                  # Go to end of inverted index
        linked_list = linked_list.nextval                   
      linked_list.nextval = Node(idx ,word_freq_in_doc[word]) # Create new node with doc idx and freq in doc








# permuterm
def invertedIndexForPermutations(inverted_index, files_with_index, Stopwords, ps):
  '''Initialise the inverted index data structure for each word and its permutations 
     to help perform wildcard searches.

     Parameters:
          **inverted_index** ( *dict* ): Dictionary containing inverted index for each word appended with a '$' at
          the end and its premutations

          **files_with_index** ( *dict* ): Dictionary with a numeric index as key and filename as value.

          **Stopwords** ( *set* ): Set of all stopwords.

          **ps** ( *PorterStemmer object* ): Class object which performs stemming.
      
      After the execution of the function, **inverted_index** will contain the inverted index for each word and
      its permutations.
  '''
  for idx, file in files_with_index.items():
    fname = file
    file = open(file, "r")
    text = file.read()
    text = remove_special_characters(text)
    text = re.sub(re.compile('\d'),'',text)
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    words = [ps.stem(word) for word in words]
      
    for word in words:                                    
      perms = list()                              # List for all permutations of that word
      n = len(word)                               #
      temp = list(word)                           # Conver word to list
      temp.append("$")                            # and append $

      i = 1                                       
      while i<=n+1:                               
        ans = "".join(temp)                       # Convert list to word
        perms.append(ans)                         # Append to perms list
        r = temp.pop()                            # Do for all permutations
        temp.insert(0,r)                          
        i+=1

      for word in perms:
        if word not in inverted_index.keys():     # Build inverted index 
          inverted_index[word] = {idx}            # for all permuatations
        else:
          inverted_index[word].add(idx) 








def permuterm(query, inverted_index):                # Parameter is single query term
  '''Get all words matching a given wildcard search query term.

     Parameters:
            **query** ( *str* ): Wildcard search query term. 

            **inverted_index** ( *dict* ): Inverted index data strucuture for all words and their permutations
            built using *invertedIndexForPermutations* function.

     Returns:
            A list of words matching the wildcard search query term.
  '''

  query = list(query)                # Convert term to list
  temp = query.copy()                      

  query.append("$")                  # Append $ to query


  if temp[-1]=="*" and temp[0] == "*":  # If * is present at first and last pos, remove * from first pos
    query.pop(0)                        
    temp.pop(0)

  elif temp[0]=="*":                    # If * is present at first pos, append at end
    t = query.pop(0)
    query.append(t)

  elif temp[-1]=="*":
    pass

  else:
    while query[-1] != "*":             # Move to last if it is somewhere in the middle
      t = query.pop(0)
      query.append(t)

  ans = list()                          # Store all words which satisfy the query (in rotated form)
  query.pop()                           # Pop *
  query = "".join(query)                # Convert to string
  print(query)                    
  n = len(query)                  
  check_list = list(inverted_index.keys())   # All words in the inverted index
  final_list = list()                        # Store all words which satisfy the query

  for word in check_list:                    # Convert words to original form
    if query == word[0:n]:
      ans.append(word)

  for word in ans:
    temp = list(word)
    if word[0]=="$":
      temp.pop(0)
    elif word[-1]=="$":
      temp.pop()

    else:
      temp = list(word)
      while temp[-1]!="$":
        t = temp.pop(0)
        temp.append(t)

      temp.pop()
      word = "".join(temp)
    word = "".join(temp)
    final_list.append(word)

  return final_list             # return words






def documents(different_words, connecting_words, unique_words_all, files_with_index, linked_list_data):             # different words - query terms, connecting words - boolean oper
  '''Get the final result vector.

     Parameters:
            **different_words** ( *list* ): List of search words in the Boolean query.

            **connecting_words** ( *list* ): List of connecting words/Boolean operators in the query.
      
     Returns:
            A list of 0's and 1's with size equal to the number of files in the dataset.
            If the entry at position i is 1, the document with index i satisfies the query and
            if it is 0, it doesn't.
  '''
  print(connecting_words)                                    
  total_files = len(files_with_index)                         
  zeroes_and_ones = []                                        # Result vector
  zeroes_and_ones_of_all_words = []                           # Result vector for all words stored as a list
  for word in (different_words):                              # process each word in query terms                             
      if word.lower() in unique_words_all:                    # if word exists in corpus
          zeroes_and_ones = [0] * total_files                 # Initialise bitmap with all 0s
          linkedlist = linked_list_data[word].head            # Head of inverted index of that word
          # print(word) 
          while linkedlist.nextval is not None:                 # Put 1 in the bitmap
              zeroes_and_ones[linkedlist.nextval.doc - 1] = 1   # if the word exists in the corresponding
              linkedlist = linkedlist.nextval                   # document and advance pointer
          zeroes_and_ones_of_all_words.append(zeroes_and_ones)  # Append bitmap for that word to list of all bitmaps
      else:
          zeroes_and_ones_of_all_words.append([0] * total_files)

  # print(zeroes_and_ones_of_all_words)
  for word in connecting_words:                                  # Processing boolean operators
      word_list1 = zeroes_and_ones_of_all_words[0]              
      word_list2 = zeroes_and_ones_of_all_words[1]               
      if word == "and":                                          
          bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,word_list2)]
          zeroes_and_ones_of_all_words.remove(word_list1)
          zeroes_and_ones_of_all_words.remove(word_list2)
          zeroes_and_ones_of_all_words.insert(0, bitwise_op);
      elif word == "or":
          bitwise_op = [w1 | w2 for (w1,w2) in zip(word_list1,word_list2)]
          zeroes_and_ones_of_all_words.remove(word_list1)
          zeroes_and_ones_of_all_words.remove(word_list2)
          zeroes_and_ones_of_all_words.insert(0, bitwise_op);
      elif word == "not":
          bitwise_op = [not w1 for w1 in word_list2]
          bitwise_op = [int(b == True) for b in bitwise_op]
          zeroes_and_ones_of_all_words.remove(word_list2)
          zeroes_and_ones_of_all_words.remove(word_list1)
          bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,bitwise_op)]

  zeroes_and_ones_of_all_words.insert(0, bitwise_op);              # Final bitmap
          
  files = []                                                                             
  # print(zeroes_and_ones_of_all_words)
  lisa = zeroes_and_ones_of_all_words[0]
  cnt = 1
  for index in lisa:
      if index == 1:
          files.append(files_with_index[cnt])
      cnt = cnt+1
      
  return files                                             # Return files satisfying query







