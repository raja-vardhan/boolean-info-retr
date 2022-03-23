class Node:                                       # Node in the inverted index
    '''
        A node of the inverted index data structure.
    '''
    def __init__(self ,docId, freq = None):
        self.freq = freq
        '''Frequency of the word in document with index = docID'''
        self.doc = docId
        '''Index of document in which the word occurs'''
        self.nextval = None
    
class SlinkedList:                                 # Head of inverted index
    '''
        Data structure to initialise head pointer to the inverted index list.
    '''
    def __init__(self ,head = None):
        self.head = head
        '''Pointer to the inverted index list'''