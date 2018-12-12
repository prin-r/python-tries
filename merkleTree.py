from hashlib import sha256

class Node(object):
    def __init__(self, left, right, key, value):
        self.left = left
        self.right = right
        self.key = key
        self.value = value
        
    def print_tree_bf(self):
        arr = [self]
        n = len(arr)
        while len(arr) > 0:
            s = ""
            for i in range(0,n,1):
                if arr[i] is not None:
                    s += 'Node({},{}) '.format(arr[i].key,arr[i].value)
                    arr.append(arr[i].left)
                    arr.append(arr[i].right)
            print(s)
            arr = arr[n:]
            n = len(arr)

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

        return sha256(hashLeft + hashRight + key + value).digest()
            
class MerkleTree(object):
    
    def __init__(self):
        self.root = Node(None, None, None, None)
    
    def insert(self, key, value):
        currentNode = self.root;
        for i in range(0, len(key)):    
            if key[i] == '0':
                if currentNode.left is None:
                    currentNode.left = Node(None,None,key[i],None)
                currentNode = currentNode.left
            elif key[i] == '1':
                if currentNode.right is None:
                    currentNode.right = Node(None,None,key[i],None)
                currentNode = currentNode.right
                
            if i == len(key) - 1:
                currentNode.key = key
                currentNode.value = value
                    
    
    def print_tree(self):
        return self.root.print_tree()
    
    def print_tree_bf(self):
        self.root.print_tree_bf()
    
    def get_hash_from_node(node):
        if node is None:
            return 
    
    def get_proof(self, key):
        proofs = []
        currentNode = self.root
        for i in range(0,len(key)):
            
            if currentNode is None:
                break
                
            hashLeft = b''
            hashRight = b''
            k = b''
            v = b''
            
            if (currentNode.left is not None):
                hashLeft = currentNode.left.get_hash()
            if (currentNode.right is not None):
                hashRight = currentNode.right.get_hash()
            if currentNode.key is not None:
                k = currentNode.key.encode('utf-8')
            if currentNode.value is not None:
                v = currentNode.value.to_bytes(32, byteorder='big')
                
            if key[i] == '0':
                currentNode = currentNode.left
                proofs.append([b'',hashRight,k,v])
            else :
                currentNode = currentNode.right
                proofs.append([hashLeft,b'',k,v])
            
        return proofs[::-1]
    
    def get_root(self):
        return self.root.get_hash()
    
    
def verify(root, key, value, proof):
    
    k = key.encode('utf-8')
    v = value.to_bytes(32, byteorder='big')
    
    rKey = key[::-1]
    rKey = rKey[1:]+rKey[:1]

    
    h = sha256(b'' + b'' + k + v).digest()
    
    for i in range(0,len(proofs)):
        if rKey[i] == '0':
            h = sha256(h + proofs[i][1] + proofs[i][2] + proofs[i][3]).digest()
        elif rKey[i] == '1':
            h = sha256(proofs[i][0] + h + proofs[i][2] + proofs[i][3]).digest()
            
    print (h.hex())
    print (h.hex() == root)

if __name__ == '__main__':
    m = MerkleTree()
    
    m.insert('0000', 10)
    m.insert('0100', 20)
    m.insert('1111', 25)
    m.insert('0010', 30)
    m.insert('0111', 40)

    #print(m.print_tree())
    m.print_tree_bf()
    print(m.get_root().hex())
    
    key = '0000'
    value = 10
    
    proofs = m.get_proof(key)
    for i in range(len(proofs)):
        print (proofs[i])
    
    verify(m.get_root(), key, value, proofs)
