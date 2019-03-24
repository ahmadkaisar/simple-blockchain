from lib import *
import json

############# Test Backup ################
# blockchain = BlockChain(pattern='1', difficulty=4)
# t1 = Transactions()
# t2 = Transactions()
# t1.add(Value('addr1', 'addr2', b'100'))
# t1.add(Value('addr1', 'addr2', b'50'))
# t1.add(Value('addr2', 'addr1', b'70'))
# t2.add(Value('addr1', 'addr2', b'20'))
# t2.add(Value('addr2', 'addr1', b'30'))
# block = Block(t1, prev_hash=blockchain.last_block.block.hash)

# # example add block to blockchain but block not mine yet
# blockchain.add(block)

# # mine block
# Mine(block).sequence(pattern=blockchain.pattern, difficulty=blockchain.difficulty)
# blockchain.add(block)
# block = Block(t2, prev_hash=blockchain.last_block.block.hash)
# Mine(block).sequence(pattern=blockchain.pattern, difficulty=blockchain.difficulty)
# blockchain.add(block)

# # example add new block with invalid prev hash
# block = Block(t2, prev_hash='12345678')
# Mine(block).sequence(pattern=blockchain.pattern, difficulty=blockchain.difficulty)
# blockchain.add(block)
# blockchain.describe()
# print(blockchain.validate())
# blockchain.backupFile()
##########################################


########### Test Recover #################
blockchain = BlockChain().recoverBackupFile()
print(blockchain.validate())
blockchain.describe()
##########################################