from GetTrie import GetRouteTrie
class GetHandler:
    getRouteTrie = GetRouteTrie()
    def __init__(self):
        pass
        
    def add_routes(self, path, handler):
        GetHandler.getRouteTrie.insertNode(path, handler)

    def handleRequest(self, path):
        # We are getting the handler function mapped in the trie, So the '()' are nececcary to get the respnse
        getFunction = GetHandler.getRouteTrie.findNode(path)
        if getFunction is not None:
            return getFunction()
        else:
            return "HTTP/1.1 400 Bad Request\r\nContent-Length: 11\r\n\r\nBad Request"        
    

    
