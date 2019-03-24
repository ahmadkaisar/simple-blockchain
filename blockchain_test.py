from lib import *
import json

#################################################### Test Backup ###########################################################################
blockchain = BlockChain(pattern='1', difficulty=4)
t1 = Transactions()
t2 = Transactions()
t1.add(Transaction(value=Value('addr1', 'addr2', b'100')))
t1.add(Transaction(value=Value('addr1', 'addr2', b'50')))
t1.add(Transaction(value=Value('addr2', 'addr1', b'70')))
t2.add(Transaction(value=Value('addr1', 'addr2', b'20')))
t2.add(Transaction(value=Value('addr2', 'addr1', b'30')))
block = Block(prev_hash=blockchain.last_block.block.hash, transactions=t1)

# example add unmined block to blockchain
blockchain.add(block)

# mine block
pending_block1 = Block(prev_hash=blockchain.last_block.block.hash)
Mine('addr1', block, pending_block1).sequence(difficulty=blockchain.difficulty, pattern=blockchain.pattern, reward=blockchain.mining_reward)
blockchain.add(block)
blockchain.add(pending_block1)

pending_block2 = Block(prev_hash=blockchain.last_block.block.hash)
block = Block(prev_hash=blockchain.last_block.block.hash, transactions=t2)
Mine('addr2', block, pending_block2).sequence(difficulty=blockchain.difficulty, pattern=blockchain.pattern, reward=blockchain.mining_reward)
blockchain.add(block)
blockchain.add(pending_block2)

# example add new block with invalid prev hash
pending_block3 = Block(prev_hash=blockchain.last_block.block.hash)
block = Block(prev_hash='12345678', transactions=t2)
Mine('addr3', block, pending_block3).sequence(pattern=blockchain.pattern, difficulty=blockchain.difficulty, reward=blockchain.mining_reward)
blockchain.add(block)
blockchain.add(pending_block3)

print('[*] addr1 balance', blockchain.getBalance('addr1'))
print('[*] addr2 balance', blockchain.getBalance('addr2'))

# blockchain.describe()
# print(blockchain.validate())
############################################################################################################################################