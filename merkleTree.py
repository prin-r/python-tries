from hashlib import sha256

class Node(object):
    def __init__(self, left, right, key, value):
        self.left = left
        self.right = right
        self.key = key
        self.value = value

    def print_tree(self):
        def getPrint(val):
            if val is None:
                return 'None'
            return val.print_tree()
        
        return 'Node( {} , {} , {} , {} )'.format(
            getPrint(self.left), getPrint(self.right), self.key, self.value)
    
    def get_hash(self):
        hashLeft = b''
        hashRight = b''
        key = b''
        value = b''
        if (self.left is not None):
            hashLeft = self.left.get_hash()
        if (self.right is not None):
            hashRight = self.right.get_hash()
        if self.key is not None:
            key =  self.key.encode('utf-8')
        if self.value is not None:
            value =  self.value.to_bytes(32, byteorder='big')
        return sha256(
            hashLeft + hashRight + key + value
        ).digest()
            
    

class MerkleTree(object):
    
    def __init__(self):
        self.root = Node(None, None, None, None)
    
    def insert(self, key, value):
        currentNode = self.root;
        for i in range(0, len(key)):
            if key[i] == '0':
                if currentNode.left is None:
                    currentNode.left = Node(None,None,key[i:],value)
                    break
                else :
                    currentNode = currentNode.left
            elif key[i] == '1':
                if currentNode.right is None:
                    currentNode.right = Node(None,None,key[i:],value)
                    break
                else :
                    currentNode = currentNode.right
                    
    
    def print_tree(self):
        return self.root.print_tree()
    
    def get_proof(self, key):
        pass
    
    def get_root(self):
        return self.root.get_hash()
    
    
def verify(self, root, key, value, proof):
     pass


if __name__ == '__main__':
    m = MerkleTree()
    
    m.insert('00000', 10)
    m.insert('01000', 20)
    m.insert('00100', 30)
    
    print(m.print_tree())
    print(m.get_root().hex())
    
    m.insert('10110110000010001111', 100)
    m.insert('10110111000010001111', 200)
    m.insert('00110111000010001111', 300)
    
    root = m.get_root()
    print('root', root)
    
    #pf = m.get_proof('10110111000010001111')
    #print(verify(root, '10110111000010001111', 200, pf))
    #print(verify(root, '10110111000010001111', 100, pf))
