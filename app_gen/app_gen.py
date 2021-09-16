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
