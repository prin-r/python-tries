from hashlib import sha256

def get_hash(left, right):
    if left is 0 and right is 0:
        return 0
    return int(sha256(left.to_bytes(32, byteorder='big')+right.to_bytes(32, byteorder='big')).hexdigest(), 16)

class Smt(object):
    def __init__(self):
        self.hash_map = {
            0: (0,0)
        }
        self.root_hash = 0

    def insert(self, key, value):
        self.root_hash = self._insert(self.root_hash, key, value)
    
    def _insert(self, current_hash, key, value):
        if len(key) <= 0:
            return value
        else :
            left_hash, right_hash = self.hash_map[current_hash]
            if key[0] is '0':
                left_hash = self._insert(left_hash, key[1:], value)
            else :
                right_hash = self._insert(right_hash, key[1:], value)
            
            if current_hash != 0 and current_hash in self.hash_map:
                del self.hash_map[current_hash]
            new_hash = get_hash(left_hash,right_hash)
            self.hash_map[new_hash] = (left_hash,right_hash)
            return new_hash

    def get_proof(self, key):
        current_hash = self.root_hash
        proofs = []
        for k in key:
            left , right = self.hash_map[current_hash]
            if k is '0':
                current_hash = left
                proofs.append(right)
            else :
                current_hash = right
                proofs.append(left)
        return proofs

    def printTree(self, depth):
        queue = [self.root_hash]
        n = len(queue)
        while n > 0 and depth >= 0:
            for i in range(0,n,1):
                print (queue[i])
                if queue[i] in self.hash_map:
                    left , right = self.hash_map[queue[i]]
                    queue.append(left)
                    queue.append(right)
            queue = queue[n:]
            n = len(queue)
            depth -= 1
            print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

def printAllKeyValue(smt):
    for k, v in smt.hash_map.items():
        print (k)
        print (v)
        print ("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("..............")

def verify(proofs, root_hash, key, value):
    current_hash = value
    for i in range(len(key) - 1,-1,-1):
        if key[i] is '0':
            current_hash = get_hash(current_hash, proofs[i])
        else :
            current_hash = get_hash(proofs[i], current_hash)

    return current_hash == root_hash

if __name__ == "__main__":
    smt = Smt()

    smt.insert('0000',100)
    smt.insert('1100',1100)

    key = '0000'
    val = 100

    smt.printTree(4)

    proofs = smt.get_proof(key)

    print (verify(proofs, smt.root_hash, key, val))

    print (proofs)
                
    print ('end')
