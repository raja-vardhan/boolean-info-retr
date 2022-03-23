import re

def finding_all_unique_words_and_freq(words):
    '''Find all the unique words and their frequencies in a string.
        
        Parameters:
          **words** ( *str* ): String to be searched for unique words.
        
        Returns:
          A dictionary with key as a word and value as frequency for that word
          for each word in the parameter **words**.
    '''
    words_unique = []   # array to store unique words in 'words'
    word_freq = {}      # dictionary to store frequency of each word in 'words'

    for word in words:               
        if word not in words_unique:        # Fill words_unique array
            words_unique.append(word)
    
    for word in words_unique:
        word_freq[word] = words.count(word)  # Fill word_freq dict
    return word_freq

def finding_freq_of_word_in_doc(word,words):  # Find count of 'word' in 'words'
  '''Get the number of times a word occurs in a string.
    
    Parameters:
        **word** ( *str* ): String to find

        **words** ( *str* ): String to be searched for finding 'word'
    
    Returns:
      Number of occurences of *word* in *words*.

  '''
  return words.count(word)
        
def remove_special_characters(text):          # Remove all chars
  '''Remove special characters in a string.

     Parameters:
          **text** ( *str* ): String to remove special characters from.
      
     Returns:
          Modified string which contains only alphanumeric characters from the original string.
  '''
  regex = re.compile('[^a-zA-Z0-9\s]')      # except alphanumeric and spaces
  text_returned = re.sub(regex,'',text)
  return text_returned

def contains_star(word):                      # Check if the word contains a *
  '''Find if the char * appears in a word.
     Parameters:
          **word** ( *str* ): String to be searched.
      
     Returns:
          Boolean value True if * occurs in the string *word* and False otherwise.
  '''
  for v in word:
    if v=="*":
      return True

  return False

  
def edit_distance(word1, word2):              # edit distance b/w word1 and word2
  '''Find the edit distance between two strings.

      Parameters:
        **word1** ( *str* ): First string
        **word2** ( *str* ): Second string

      Returns:
        Edit distance between the two strings.
  '''
  l1 = len(word1)
  l2 = len(word2)
  if l1 == 0:
    return l2
  if l2 == 0:
    return l1

  dp = [[0 for i in range(l2 + 1)] for j in range(l1 + 1)]

  for x in range(l2 + 1):
    dp[0][x] = x
  for x in range(l1 + 1):
    dp[x][0] = x
  
  for i in range(1, l1 + 1):
    for j in range(1, l2 + 1):
      if word1[i-1] == word2[j-1]:
        dp[i][j] = dp[i-1][j-1]
      else:
        dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
  
  return dp[l1][l2]
