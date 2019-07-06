import hashlib
import json
from datetime import datetime
import numpy as np

class mchain(list):

    min_length = 0
    def __init__(self, min_length = 3, *args):
        """"""
        list.__init__(self, *args)
        self.append(self.createGenesisBlock())
        self.min_length = min_length


    def createGenesisBlock(self):
        gb = mchain_block(0,'Genesis Block', 0)
        gb.hash = gb.generateHash(self.min_length)
        return gb

    def getLatestBlock(self):
        return self[-1]

    def addBlock(self, newBlock):
        """
        :type newBlock: mchain_block
        """
        prevBlock = self.getLatestBlock()
        newBlock.previousHash =prevBlock.hash
        newBlock.hash = newBlock.generateHash(self.min_length)
        self.append(newBlock)

    def isChainValid(self):
        for i in range(1,len(self)):
            currentBlock = self[i]
            prevBlock = self[i-1]

            if (currentBlock.hash != currentBlock.calculateHash()):
                print(f'Block_id({currentBlock.block_id}), hash={currentBlock.hash}')
                print(f'Invalid current hash: {currentBlock.calculateHash()}')
                return False
            if (prevBlock.hash != currentBlock.previousHash):
                print(f'Invalid previous hash({currentBlock.block_id}): {prevBlock.hash} : {currentBlock.previousHash}')
                return False
        return True

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class mchain_block():

    def __init__(self, block_id, data, previousHash = ''):
        """"""
        self.block_id = str(block_id)
        self.timestamp = datetime.utcnow().strftime('%Y-%m-%d%H:%M%S')
        self.data = json.dumps(data)
        self.previousHash = str(previousHash)
        self.hash = ''
        self.nonce = ''

    def calculateHash(self):
        h = hashlib.sha256()
        for _ in [self.block_id.encode(),
        self.previousHash.encode(),
        self.timestamp.encode(),
        self.data.encode(),
        self.nonce.encode()]:
            h.update(_)
        return h.hexdigest()

    def generateHash(self, min_zeros):
        candidate_hash = ""
        now = datetime.now()
        while not str(candidate_hash).startswith("0"*min_zeros):
            self.nonce = str(np.random.rand())
            candidate_hash = self.calculateHash()
        print(f'Found a good nonce {self.nonce}.  Hash = {candidate_hash} ')
        print(f'Time to find hash = {(datetime.now()-now).seconds} seconds')
        return candidate_hash

    def hash_string(self,s):
        return


if __name__ == "__main__":
    nChain = mchain(min_length=5)
    nChain.addBlock(mchain_block(1,'someData'))
    nChain.addBlock(mchain_block(2,'otherData'))
    nChain.addBlock(mchain_block(3,'otherData2'))

    print(f'{nChain.toJSON()}')
    print(f'Unmodified chain is good? {nChain.isChainValid()}')

    nChain[1].data = 'otherData 2'
    print(f'Modified chain is good? {nChain.isChainValid()}')

