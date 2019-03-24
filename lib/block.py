from .requirement import *
from .transaction import *

class Header:
	def __init__(self, prev_hash=None):
		self.prev_hash = prev_hash
		self.timestamp = str(datetime.datetime.utcnow())
		self.nonce = 0
	def convert(self):
		return {
			'prev_hash':self.prev_hash,
			'timestamp':self.timestamp,
			'nonce':self.nonce
		}
	def decodeJson(self, data):
		self.prev_hash = data['prev_hash']
		self.timestamp = data['timestamp']
		self.nonce = data['nonce']

class Block:
	def __init__(self, transactions=Transactions(), prev_hash=None):
		self.header = Header(prev_hash)
		self.transactions = transactions
		self.hash = None
	def convert(self):
		return {
			'header':self.header.convert(),
			'transactions':self.transactions.convert(),
			'hash':self.hash
		}
	def decodeJson(self, data):
		self.header.decodeJson(data['header'])
		self.transactions.decodeJson(data['transactions'])
		self.hash = data['hash']