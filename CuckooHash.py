from BitHash import BitHash1
from BitHash import BitHash2
import math 
import random

# bucket object contains key and data attributes
class Bucket(object):
    def __init__(self, key, data):
        self.key = key
        self.data = data
        
class HashTab(object):
    # this hash table is internally represented as an array
    # intially, the array contains Nones, but when buckets are inserted, there will
    # be Bucket objects at  those locations in the array
    def __init__(self, size):
        self.hashArray = [None] * size
        
        
    def findInHash1(self, key):
        # hash in order to find the location where the key might be
        location = BitHash1(key) % len(self.hashArray)
       
        # if the bucket is in the hash table, return the location and the key. 
        # Otherwise, return None
        if self.hashArray[location] != None:
            return location, self.hashArray[location].key
        return location, None
        
    
    def findInHash2(self, key):
        # hash in order to find the location where the key might be
        location = BitHash2(key) % len(self.hashArray)
        
        # if the bucket is in the hash table, return the location and the key. 
        # Otherwise, return None
        if self.hashArray[location] != None:
            return location, self.hashArray[location].key
        return location, None        
           
    
class CuckooHash(object):
    # constructor: initializing both hash tables with a size of 50 (size may 
    # change later on)
    def __init__(self, size = 50):
        self.__h1 = HashTab(size)
        self.__h2 = HashTab(size)
        # the number of buckets in EACH Hash Table
        self.__size = size
    
    # returns the length of each hash table    
    def __len__(self): return self.__size
       
    def __str__(self):
        onlyKeys1 = []
        onlyKeys2 = []
        
        # loop through each hashArray and append only the keys to their respective lists
        for i in self.__h1.hashArray:
            if i:
                onlyKeys1.append(i.key)
            else: onlyKeys1.append(None)
            
        for i in self.__h2.hashArray:
            if i:
                onlyKeys2.append(i.key)
            else: onlyKeys2.append(None)
            
        # return string representations of both of the hash tables
        return "Table1: " + str(onlyKeys1) + "\n" + "Table2: " + str(onlyKeys2)
        
        
    def __rehash(self):
        # save all the previously inserted buckets into a new list
        insertedBuckets = self.__h1.hashArray + self.__h2.hashArray
                
        # double the size of the hash table
        self.__size *= 2
        self.__h1 = HashTab(self.__size)
        self.__h2 = HashTab(self.__size)
        
        
        # reinsert all the values
        for i in insertedBuckets:
            if i != None:
                self.insert(i.key, i.data)
            
    def insert(self, key, data):
        # if the key, data pair has already been inserted, don't insert
        if self.find(key) != None and self.find(key) == data: return False
        
        # this is the maximum amount of times that we will allow the loop to run
        # before rehashing
        maxLoop = 3*(math.log(self.__size, 1.5))
        
        # the bucket object we want to insert
        bucket = Bucket(key, data)
        
        # the locations of the bucket in each hashArray
        location1 = BitHash1(key) % len(self.__h1.hashArray)
        location2 = BitHash2(key) % len(self.__h2.hashArray)
        
        # loop maxLoop times
        for i in range(int(maxLoop)):
            
            # swap whatever is in the bucket with the bucket being inserted
            temp = self.__h1.hashArray[location1]
            self.__h1.hashArray[location1] = bucket
            bucket = temp
            
            # if there was nothing in the bucket, stop looping 
            if bucket == None: return True
            
            # reset the locations to the current bucket
            location1 = BitHash1(bucket.key) % len(self.__h1.hashArray)
            location2 = BitHash2(bucket.key) % len(self.__h2.hashArray)
            
            # if the bucket gets kicked out, try putting it into its alternate 
            # space in the second hash table
            temp1 = self.__h2.hashArray[location2]
            self.__h2.hashArray[location2] = bucket
            bucket = temp1 
            
            # if there was nothing in the bucket, stop looping
            if bucket == None: return True
            
            # before looping again, set bucket1 and bucket2 to the locations of the 
            # bucket that was recently kicked out
            location1 = BitHash1(bucket.key) % len(self.__h1.hashArray)
            location2 = BitHash2(bucket.key) % len(self.__h2.hashArray)            
            
        # if we went through the loop without inserting in an empty space, rehash     
        self.__rehash()
        
        # try inserting again with the bucket that was last kicked out
        self.insert(bucket.key,bucket.data)
        
                
    def find(self, key):    
        # invoke find on both hash tables which return the bucket location and 
        # the data if it's there. 
        location1, key1 = self.__h1.findInHash1(key)
        location2, key2 = self.__h2.findInHash2(key)
        
        # check if there was a key in either of the hash tables 
        # if so, return the data
        if key1 == key: return self.__h1.hashArray[location1].data
        elif key2 == key: return self.__h2.hashArray[location2].data
        
        # if not, return None
        return None
        
    
    def delete(self, key):
        # invoke find on both hash tables which return the bucket location and 
        # the key if it's there. 
        location1, key1 = self.__h1.findInHash1(key)
        location2, key2 = self.__h2.findInHash2(key)
        
        # if there is a key in the bucket location of either hash table, set that 
        # bucket to None and return True(bc the deletion was a success), otherwise return False
        if key1 == key: 
            self.__h1.hashArray[location1] = None
            return True
        elif key2 == key: 
            self.__h2.hashArray[location2] = None
            return True
        return False


