import sys
sys.path.insert(0, 'C:/Users/rafae/OneDrive/Desktop/Vasado/SIM/IoTCOMMs/app_gen')

from app_gen import Node , APP
from collections import OrderedDict
import string
import random
import graphviz
import numpy as np

class LRUCache:
 
    # initialising capacity
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
 
    #function to make a reference to to the Topic Hash
    #if not found, return -1
    #else return the node
    def get(self, key , topic):
        
        if key not in self.cache:
            #print("miss")
            return [0 , None]
        elif self.cache[key].topic != topic:
            #print("conf")
            return [1 , None]
        else:
            #print("hit")
            self.cache.move_to_end(key)
            return [2 , self.cache[key]]
    
    def put(self, key: int, value: Node) -> None:
         
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)
 
        
class CacheController:
    def __init__(self, dev_cache_capacity, area_cache_capacity):
        self.miss_dict = ["cache miss" , "cache miss conflict"]
        self.dev_cache_capacity = dev_cache_capacity
        self.area_cache_capacity = area_cache_capacity
        self.dev_cache = LRUCache(dev_cache_capacity)
        self.area_cache = LRUCache(area_cache_capacity)
        self.stats = {}
        self.stats["dev"] = []
        self.stats["dev"].append({"cache miss":0 , "cache miss conflict":0})
        
        self.stats["area"] = []
        for depth in range(6):
            self.stats["area"].append({"cache miss":0 , "cache miss conflict":0})
            self.stats["area"][depth]["cache miss"] = 0
            self.stats["area"][depth]["cache miss conflict"] = 0
    
    def stats_update(self, stats_name, cache_type, index):
        
        self.stats[cache_type][index][stats_name] = self.stats[cache_type][index][stats_name] + 1
        
    def FE2HASH(self , topic):
        areas = topic.split('/')
        areas.pop()
        areas.pop(0)
        #Check dev chache for topic
        topic_key = hash(topic) % self.dev_cache_capacity 
        #print("key " , topic_key, "topic " , topic)
        node = self.dev_cache.get(topic_key , topic)
        #topic missed
        if node[0] < 2:
            self.stats_update(self.miss_dict[node[0]] , "dev" , 0)
            node = Node("" , topic)
            self.dev_cache.put(topic_key , node)
        #check area cache for areas
        for depth , area in enumerate(areas):
            key = hash(area) % self.area_cache_capacity
            node = self.area_cache.get(key , area)
            
            if node[0] < 2:
                print("key " , key, "topic " , area , " depth " , depth)
                self.stats_update(self.miss_dict[node[0]] , "area" , depth)
                node = Node("" , area)
                self.area_cache.put(key , node)

    def print_stats(self):
        for cache , value in self.stats.items():
            for stat_type in value:
                print(cache , stat_type)


def print_tree(node , dot):
    if len(node.children) == 0:
        return
    dot.node(node.topic , node.topic)
    for child in node.children:
        dot.node(child.topic , child.topic)
        
        dot.edge(node.topic , child.topic)
        print_tree(child , dot)

cache_controller = CacheController(10 , 100) 

