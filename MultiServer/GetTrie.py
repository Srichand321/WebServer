class Trie():
    def __init__(self):
        self.children = {}
        self.handler = None

class GetRouteTrie():
    def __init__(self):
        self.root = Trie()
    
    def insertNode(self, path, handler):
        node = self.root
        words = path.split("/")
        print(words)
        for word in words[1:]:
            if(word not in node.children):
                node.children[word] = Trie()
            node = node.children[word]
        node.handler = handler
    
    def findNode(self, path):
        node = self.root
        words = path.split("/")
        for word in words[1:]:
            if(word in node.children):
                node = node.children[word]
            elif("*" in node.children):
                node = node.children["*"]
            else:
                return None
        return node.handler if node.handler is not None else None

    
