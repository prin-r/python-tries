from hashlib import sha256
from random import shuffle , randint

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
            
            newHash = getHash(left,right)
            if currentHash != 0 and currentHash in self.mapping:
                 del self.mapping[currentHash]
            self.mapping[newHash] = (left,right)
            return newHash

    def getProof(self, key):
        currentHash = self.root
        proofs = []
        mask = 0
        for i in range(0,len(key)):
            left , right = self.mapping[currentHash]
            if key[i] is '0':
                currentHash = left
                if right != 0:
                    proofs += [right]
                else :
                    mask = mask | (1<<i)
            else :
                currentHash = right
                if left != 0:
                    proofs += [left]
                else :
                    mask = mask | (1<<i)
        return [mask] + proofs

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
    mask = proofs[0]
    proofVal = 0
    proofIndex = len(proofs) - 1
    for i in range(len(key) - 1,-1,-1):
        if mask & (1<<(i)) != 0:
            proofVal = 0
        else :
            proofVal = proofs[proofIndex]
            proofIndex -= 1

        if key[i] is '0':
            currentHash = getHash(currentHash, proofVal)
        else :
            currentHash = getHash(proofVal, currentHash)

    return currentHash == root

def randBigValRange():
    #value must be unique
    return randint(1, 1<<128)

def getKeys(keySize, key):
    if keySize <= 0:
        return [key]
    return getKeys(keySize - 1, key + '0') + getKeys(keySize - 1, key + '1')

def testSmt(keySize, maxIteration):
    keys = getKeys(keySize, '')

    for iteration in range(0,maxIteration,1):
        print ("iteration = ", iteration)

        smt = Smt()
        shuffle(keys)
        inclusionSize = randint(0, len(keys))

        #max inclusion
        if inclusionSize > 64:
            inclusionSize = 64

        inclusionKeys = keys[:inclusionSize]
        nonInclusionKeys = keys[inclusionSize:]

        inclusionVal = []
        for k in inclusionKeys:
            inclusionVal += [randBigValRange()]

        for i in range(0,inclusionSize,1):
            smt.insert(inclusionKeys[i], inclusionVal[i])

        #proof inclusion
        for i in range(0,inclusionSize,1):
            proofs = smt.getProof(inclusionKeys[i])
            if not verify(proofs, smt.root, inclusionKeys[i], inclusionVal[i]):
                return False
        
        for i in range(0,inclusionSize,1):
            proofs = smt.getProof(inclusionKeys[i])
            if verify(proofs, smt.root, inclusionKeys[i], 0):
                return False

        #proof non-inclusion
        for i in range(0,len(nonInclusionKeys),1):
            proofs = smt.getProof(nonInclusionKeys[i])
            if not verify(proofs, smt.root, nonInclusionKeys[i], 0):
                return False

        for i in range(0,len(nonInclusionKeys),1):
            proofs = smt.getProof(nonInclusionKeys[i])
            if verify(proofs, smt.root, nonInclusionKeys[i], randBigValRange()):
                return False
    
    return True

if __name__ == "__main__":
    smt = Smt()

    smt.insert('0000',100)
    smt.insert('0001',2)
    smt.insert('0111',77)
    smt.insert('1000',9)
    smt.insert('1111',223)

    key = '0100'
    val = 0

    smt.printTree(4)

    proofs = smt.getProof(key)
    print (verify(proofs, smt.root, key, val))
    print (proofs)

    isPassTest = testSmt(10, 8192)
    print ("isPassTest =", isPassTest)
    
    print ('end')
