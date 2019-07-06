import datetime
import hashlib
import json

import numpy as np


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