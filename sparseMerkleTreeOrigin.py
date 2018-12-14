from hashlib import sha256

def getHash(left, right):
    if left is 0 and right is 0:
        return 0
    return int(sha256(left.to_bytes(32, byteorder='big')+right.to_bytes(32, byteorder='big')).hexdigest(), 16)

class Smt(object):
    def __init__(self):
        self.mapping = {
            0: (0,0)
        }
        self.root = 0

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)
    
    def _insert(self, currentHash, key, value):
        if len(key) <= 0:
            return value
        else :
            left, right = self.mapping[currentHash]
            if key[0] is '0':
                left = self._insert(left, key[1:], value)
            else :
                right = self._insert(right, key[1:], value)
            
            if currentHash != 0 and currentHash in self.mapping:
                del self.mapping[currentHash]
            newHash = getHash(left,right)
            self.mapping[newHash] = (left,right)
            return newHash

    def getProof(self, key):
        currentHash = self.root
        proofs = []
        for k in key:
            left , right = self.mapping[currentHash]
            if k is '0':
                currentHash = left
                proofs += [right]
            else :
                currentHash = right
                proofs += [left]
        return proofs

    def printTree(self, depth):
        queue = [self.root]
        n = len(queue)
        while n > 0 and depth >= 0:
            for i in range(0,n,1):
                print (queue[i])
                if queue[i] in self.mapping:
                    left , right = self.mapping[queue[i]]
                    queue += [left]
                    queue += [right]
            queue = queue[n:]
            n = len(queue)
            depth -= 1
            print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def printAllKeyValue(smt):
    for k, v in smt.mapping.items():
        print (k)
        print (v)
        print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("..............")

def verify(proofs, root, key, value):
    currentHash = value
    for i in range(len(key) - 1,-1,-1):
        if key[i] is '0':
            currentHash = getHash(currentHash, proofs[i])
        else :
            currentHash = getHash(proofs[i], currentHash)

    return currentHash == root

if __name__ == "__main__":
    smt = Smt()

    smt.insert('0000',100)
    smt.insert('1100',1100)

    key = '1100'
    val = 1100

    smt.printTree(4)

    proofs = smt.getProof(key)

    print (verify(proofs, smt.root, key, val))

    print (proofs)
                
    print ('end')
