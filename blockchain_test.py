from lib import *
import json

blockchain = BlockChain(pattern='111111')
# t1 = Transaction()
# t2 = Transaction()
# t1.add(b'abc')
# t1.add(b'def')
# t1.add(b'ghi')
# t2.add(b'masamune')
# t2.add(b'kenji')
# blockchain.add(Block(t1), mine=True)
# blockchain.add(Block(t2), mine=True)
# blockchain.describe()
# blockchain.backup()
blockchain = blockchain.recoverBackup()
print(blockchain.validate())