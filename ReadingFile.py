'''
Created on Jul 13, 2016

@author: Daniel
'''
from blaze.server.serialization import pickle
import pickle

def read_file():
    try:
        queue = pickle.load( open( "zhihu_queue.pickle", "rb" ) )
        return queue
    except:
        return None