import string
import random
import graphviz
import numpy as np
import json

class Node:
    def __init__(self, data , topic):
        self.data = data
        self.topic = topic
        self.parent = None
        self.children = []

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
                for p in range(n_dev):
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

f = open("config.json")
config = json.load(f)
print(config["hierarchy"])
a1 = config["hierarchy"]["dist"][0]
a2 = config["hierarchy"]["dist"][1]
a3 = config["hierarchy"]["dist"][2]
a4 = config["hierarchy"]["dist"][3]
app = APP([a1 , a2 , a3 , a4, np.random.poisson(lam=4 , size=(a4*a3*a2)).tolist()] , config["topic_size"])


dot = graphviz.Digraph(comment='Normal')
#dot.graph_attr['rankdir'] = 'LR'

if config["display_graph"]:
    print_tree(app.root, dot)
    dot.render('test-output/gen_tree.gv', view=True) 


topic_indexes = []

for i in range(len(app.devices) -1):
    topic_indexes.append(i)



for i in range(1000):
    random.shuffle(topic_indexes)
    for dev_index in topic_indexes:
        topic = app.compose_topic(app.devices[dev_index])
        
