from collections import OrderedDict
import string
import random
import graphviz
import numpy as np

class Node:
    def __init__(self, data , topic):
        self.data = data
        self.topic = topic
        self.parent = None
        self.children = []

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

class APP():
    
    def __init__(self, app_distro , topic_size):
        
        self.app = []
        self.letters = string.ascii_lowercase
        self.app_distro = app_distro
        self.root = Node("" , "city")
        self.n_topics = 0
        self.devices = []
        self.topic_size = topic_size
        self.gen_app(self.root , 1)
        
        
    
    def gen_app(self , node, k):
        
        if k + 1 > (len(self.app_distro) -1):
            return
        
        for j in range(self.app_distro[k]):
            node.children.append(Node("" , ''.join(random.choice(self.letters) for i in range(self.topic_size))))
            node.children[j].parent = node
           
            if k == (len(self.app_distro) - 2):
                
                n_dev = self.app_distro[k+1].pop()
                for shizzle in range(n_dev):
                    self.devices.append(Node("" , ''.join(random.choice(self.letters) for i in range(self.topic_size))))
                    self.devices[len(self.devices) - 1].parent = node.children[j]
                    node.children[j].children.append(self.devices[len(self.devices) - 1])
            self.gen_app(node.children[j] , k+1)
            
            
        
    def print_tree(self , node):
        
        for i in range(len(node.children) -1):
            self.print_tree(node.children[i])
            self.n_topics = self.n_topics + 1
    
    def compose_topic(self, dev):
        node = dev
        topic = dev.topic
        node = dev.parent
        while node:
            topic = node.topic + "/" + topic
            node = node.parent
        return topic

def print_tree(node , dot):
    if len(node.children) == 0:
        return
    dot.node(node.topic , node.topic)
    for child in node.children:
        dot.node(child.topic , child.topic)
        
        dot.edge(node.topic , child.topic)
        print_tree(child , dot)

cache_controller = CacheController(10 , 100) 

a1 = 1
a2 = 2
a3  = 2
a4 = 2
app = APP([a1 , a2 , a3 , a4, np.random.poisson(lam=4 , size=(a4*a3*a2)).tolist()] , 20)


dot = graphviz.Digraph(comment='Normal')
#dot.graph_attr['rankdir'] = 'LR'

print_tree(app.root, dot)

dot.render('test-output/round-table.gv', view=True) 


topic_indexes = []

for i in range(len(app.devices) -1):
    topic_indexes.append(i)



for i in range(1000):
    random.shuffle(topic_indexes)
    for dev_index in topic_indexes:
        topic = app.compose_topic(app.devices[dev_index])
        cache_controller.FE2HASH(topic)

cache_controller.print_stats()
