from hashlib import sha256

def getHash(left, right):
    if left == 0 and right == 0:
        return 0
    return int(sha256(
        left.to_bytes(32, byteorder='big') +
        right.to_bytes(32, byteorder='big')
    ).hexdigest(), 16)
    

class MerkleTree(object):
    
    def __init__(self):
        self.hash_map = {
            0: (0, 0)
        }
        self.root_hash = 0
        
    def insert(self, key, value):
        self.root_hash = self._insert(key, value, self.root_hash)
        
    def _insert(self, key, value, myHash):
        if len(key) == 0:
            return value
        else :
            leftHash, rightHash = self.hash_map[myHash]
            if key[0] == '0':
                leftHash = self._insert(key[1:],value,leftHash)
            else :
                rightHash = self._insert(key[1:],value,rightHash)
            myNewHash = getHash(leftHash,rightHash)
            self.hash_map[myNewHash] = (leftHash,rightHash)
            return myNewHash
    
    def get_proof(self, key):
        currentNodeHash = self.root_hash
        associateNodes = []
        mask = 0
        for i in range(0,len(key)):
            left, right = self.hash_map[currentNodeHash]
            if key[i] == '0':
                currentNodeHash = left
                if right != 0:
                    associateNodes.append(right)
                else:
                    mask = mask | (1 << i)
            else :
                currentNodeHash = right
                if left != 0:
                    associateNodes.append(left)
                else:
                    mask = mask | (1 << i)
        return [mask] + associateNodes
        
def verify(root, key, value, proof):
    myHash = value
    
    mask = proof[0]
    proofIndex = 1
    
    for i in range(len(key)-1, -1, -1):
        if mask & (1 << (i)) != 0:
            proofValue = 0
        else:
            proofValue = proof[proofIndex]
            proofIndex += 1
        
        if '0' == key[i]:
            myHash = getHash(myHash, proofValue)
        else:
            myHash = getHash(proofValue, myHash)
    return myHash == root

if __name__ == '__main__':
    m = MerkleTree()
    m.insert('101', 10)
    m.insert('100', 50)
    m.insert('001', 20)
    print(m.root_hash)
    # for key, val in m.hash_map.items():
    #     print(key)
    #     print(val)
    #     print('---')
        
    print (m.get_proof('101'))
    print (verify(m.root_hash, '101', 10, m.get_proof('101')))
