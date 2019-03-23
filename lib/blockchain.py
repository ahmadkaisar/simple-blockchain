from .requirement import *
from .block import *

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
			temp_blockchain.block.sequenceMine(0, 1, self.pattern)
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
		index = self.index
		block = self.block
		next_block = self.next
		try:
			while True:
				temp = block.convert()
				temp['index'] = index
				with open(path + str(index) + '.block', 'w') as f:
					json.dump(temp, f)
				if next_block is None:
					break
				index = next_block.index
				block = next_block.block
				next_block = next_block.next
			print('[*] backup to file successfully completed')
		except:
			print('[*] backup to file failed at block', index)
	def convert(self):
		index = self.index
		block = self.block
		next_block = self.next
		blockchain = []
		while True:
			temp = block.convert()
			temp['index'] = index
			blockchain += [temp]
			if next_block is None:
				break
			index = next_block.index
			block = next_block.block
			next_block = next_block.next
		return {
			'pattern':self.pattern,
			'blockchain':json.dumps(blockchain)
		}
	def describe(self):
		print('[*] describe blockchain')
		block = self.block
		next_block = self.next
		while True:
			print(block.convert())
			if next_block is None:
				break
			block = next_block.block
			next_block = next_block.next
		print('[*] end describe')
	def generateGenesis(self, genesis):
		genesis_transaction = Transaction()
		genesis_transaction.add(genesis)
		genesis_block = Block(genesis_transaction)
		genesis_block.sequenceMine(0, 1, self.pattern)
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
		while True:
			try:
				with open(path + str(index) + '.block', 'r') as f:
					temp_block = json.loads(f.read())
					temp_transaction = Transaction()
					for transaction in json.loads(temp_block['transaction']):
						temp_transaction.add(transaction['value'])
						temp_transaction.transaction[-1].timestamp = transaction['timestamp']
					if temp_blockchain is None:
						temp_blockchain = BlockChain()
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
		return temp_blockchain
	def validate(self):
		block = self.block
		next_block = self.next
		while next_block is not None:
			if block.hash != next_block.block.header.prev_hash:
				return (False, self.index, index)
			index = next_block.index
			block = next_block.block
			next_block = next_block.next
		return (True, self.index, self.last_block.index)