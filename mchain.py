import hashlib
import json
from datetime import datetime
from uu import encode


class mchain(list):

    def __init__(self, *args):
        """"""
        list.__init__(self, *args)
        self.append(self.createGenesisBlock())

    def createGenesisBlock(self):
        gb = mchain_block(0,'Genesis Block', 0)
        gb.hash = gb.calculateHash()
        return gb

    def getLatestBlock(self):
        return self[-1]

    def addBlock(self, newBlock):
        """
        :type newBlock: mchain_block
        """
        prevBlock = self.getLatestBlock()
        newBlock.lastHash =prevBlock.hash
        newBlock.hash = newBlock.calculateHash()
        self.append(newBlock)

    def isChainValid(self):
        for i in range(1,len(self)):
            currentBlock = self[i]
            prevBlock = self[i-1]

            if (currentBlock.hash != currentBlock.calculateHash()):
                print(f'Block_id({currentBlock.block_id}), hash={currentBlock.hash}')
                print(f'Invalid current hash: {currentBlock.calculateHash()}')
                return False
            if (prevBlock.hash != currentBlock.lastHash):
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

    def calculateHash(self):
        h = hashlib.sha256()
        for _ in [self.block_id.encode(), self.previousHash.encode(), self.timestamp.encode(), self.data.encode()]:
            h.update(_)
        return h.hexdigest()


if __name__ == "__main__":
    nChain = mchain()
    nChain.addBlock(mchain_block(1,'someData'))
    nChain.addBlock(mchain_block(2,'otherData'))
    nChain.addBlock(mchain_block(3,'otherData2'))

    print(f'{nChain.toJSON()}')
    print(f'Is chain valid? {nChain.isChainValid()}')

    nChain[1].data = 'otherData 2'
    print(f'Is chain valid? {nChain.isChainValid()}')
