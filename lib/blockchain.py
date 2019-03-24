from .requirement import *
from .block import *
from .mine import *

class BlockChain:
	def __init__(self, difficulty=1, genesis=b'Genesis Block', mining_reward=100, new_block=None, pattern='0'):
		self.index = 0
		self.difficulty = difficulty
		self.pattern = self.handlePattern(pattern)
		self.block = new_block if new_block is not None else self.generateGenesis(genesis)
		self.next = None
		self.mining_reward = mining_reward
		self.last_block = self
	def add(self, new_block):
		print('[*] add block')
		if new_block.hash is None:
			print('[*] add block failed')
			return
		temp_blockchain = BlockChain(new_block=new_block, pattern=self.pattern)
		if temp_blockchain.block.header.prev_hash != self.last_block.block.hash:
			print('[*] prev hash in this block is invalid')
			return
		temp_blockchain.index = self.last_block.index + 1
		self.last_block.next = temp_blockchain
		self.last_block = temp_blockchain
		self.last_block.last = self.last_block
		self.last_block.pattern = self.pattern
		blockchain = self.next
		while blockchain.next is not None:
			blockchain.last = self.last_block
			blockchain.mining_reward = self.mining_reward
			blockchain = blockchain.next
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
			'blockchain':result,
			'difficulty':self.last_block.difficulty,
			'mining_reward':self.mining_reward,
			'pattern':self.pattern
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
		genesis_transaction = Transactions()
		genesis_transaction.add(Transaction(value=Value('', '', genesis)))
		genesis_block = Block(prev_hash=0, transactions=genesis_transaction)
		Mine('', genesis_block, Block()).sequence(difficulty=self.difficulty, pattern=self.pattern, reward=0)
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
	def getBalance(self, addr):
		balance = 0
		blockchain = self
		while blockchain is not None:
			block = blockchain.block.convert()
			for transaction in block['transactions']:
				transaction = transaction['transaction']
				try:
					value = transaction['value'][2:]
					value = value[:len(value)-1]
					if transaction['fromAddress'] == addr:
						balance -= int(value)
					elif transaction['toAddress'] == addr:
						balance += int(value)
				except:
					pass
			blockchain = blockchain.next
		return balance
	def handlePattern(self, pattern):
		pattern = pattern.lower()
		pattern = ''.join([x for x in pattern if (x >= 'a' and x <= 'f') or (x >= '0' and x <= '9')])
		pattern = pattern if len(pattern) > 0 else '0'
		print('[*] accepted pattern', pattern)
		return pattern
	def validate(self):
		blockchain = self
		while blockchain.next is not None:
			if blockchain.block.hash != blockchain.next.block.header.prev_hash:
				blockchain.next = None
				return (False, self.index, self.last_block.index)
			blockchain = blockchain.next
		return (True, self.index, self.last_block.index)