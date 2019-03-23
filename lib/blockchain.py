from .requirement import *
from .block import *
from .mine import *

class BlockChain:
	def __init__(self, new_block=None, genesis=b'Genesis Block', pattern='1102'):
		self.index = 0
		self.pattern = pattern
		self.block = new_block if new_block is not None else self.generateGenesis(genesis)
		self.next = None
		self.last_block = self
	def add(self, new_block, mine=False):
		print('[*] add block offline')
		temp_blockchain = BlockChain(new_block, pattern=self.pattern)
		temp_blockchain.block.header.prev_hash = self.last_block.block.hash
		if mine is True:
			Mine(temp_blockchain.block).sequence(self.pattern, 0, 1)
		temp_blockchain.index = self.last_block.index + 1
		self.last_block.next = temp_blockchain
		self.last_block = temp_blockchain
		self.last_block.last = self.last_block
	def backup(self):
		path = 'blocks/'
		if not os.path.exists(path):
			print('[*] backup directory not exists')
			print('[*] make new directory')
			os.makedirs(path)
		blockchain = self
		try:
			while True:
				temp = blockchain.block.convert()
				temp['index'] = blockchain.index
				with open(path + str(blockchain.index) + '.block', 'w') as f:
					json.dump(temp, f)
				if blockchain.next is None:
					break
				blockchain = blockchain.next
			with open(path + 'pattern.block', 'w') as f:
				temp = {'pattern':self.pattern}
				json.dump(temp, f)
			print('[*] backup to file successfully completed')
		except:
			print('[*] backup to file failed / there\'s no remaining file')
	def convert(self):
		blockchain = self
		result = []
		while True:
			temp = blockchain.block.convert()
			temp['index'] = blockchain.index
			result += [temp]
			if blockchain.next is None:
				break
			blockchain = blockchain.next
		return {
			'pattern':self.pattern,
			'blockchain':json.dumps(result)
		}
	def describe(self):
		print('[*] describe blockchain')
		blockchain = self
		while True:
			print(blockchain.block.convert())
			if blockchain.next is None:
				break
			blockchain = blockchain.next
		print('[*] end describe')
	def generateGenesis(self, genesis):
		genesis_transaction = Transaction()
		genesis_transaction.add(genesis)
		genesis_block = Block(genesis_transaction)
		Mine(genesis_block).sequence(self.pattern, 0, 1)
		return genesis_block
	def getIndex(self, index=0):
		blockchain = self
		while index > blockchain.index:
			if blockchain.next is None:
				return {'block':None}
			blockchain = blockchain.next
		return {'block':blockchain.block.convert()}
	def getFrom(self, index=0):
		blockchain = self
		while index > blockchain.index:
			if blockchain.next is None:
				return {'pattern':self.pattern, 'blockchain':None}
			blockchain = blockchain.next
		return blockchain.convert()
	def recoverBackup(self, path='blocks/'):
		index = 0
		temp_blockchain = None
		try:
			with open(path + 'pattern.block', 'r') as f:
				pattern = json.loads(f.read())['pattern']
		except:
			pattern = self.pattern
		while True:
			try:
				with open(path + str(index) + '.block', 'r') as f:
					temp_block = json.loads(f.read())
					temp_transaction = Transaction()
					for transaction in temp_block['transaction']:
						temp_transaction.add(transaction['value'])
						temp_transaction.transaction[-1].timestamp = transaction['timestamp']
					if temp_blockchain is None:
						temp_blockchain = BlockChain(pattern=pattern)
						temp_blockchain.index = temp_block['index']
						temp_blockchain.block.transaction = temp_transaction
						temp_blockchain.block.hash = temp_block['hash']
						temp_blockchain.block.header.prev_hash = temp_block['header']['prev_hash']
						temp_blockchain.block.header.timestamp = temp_block['header']['timestamp']
						temp_blockchain.block.header.nonce = temp_block['header']['nonce']
					else:
						temp_blockchain.add(Block(temp_transaction))
						temp_blockchain.last_block.index = temp_block['index']
						temp_blockchain.last_block.block.hash = temp_block['hash']
						temp_blockchain.last_block.block.header.prev_hash = temp_block['header']['prev_hash']
						temp_blockchain.last_block.block.header.timestamp = temp_block['header']['timestamp']
						temp_blockchain.last_block.block.header.nonce = temp_block['header']['nonce']
					index += 1
			except:
				break
		if temp_blockchain is None:
			return BlockChain()
		return temp_blockchain
	def validate(self):
		blockchain = self
		while blockchain.next is not None:
			if blockchain.block.hash != blockchain.next.block.header.prev_hash:
				blockchain.next = None
				return (False, self.index, index)
			blockchain = blockchain.next
		return (True, self.index, self.last_block.index)