from .requirement import *
from .transaction import *

class Header:
	def __init__(self, prev_hash):
		self.prev_hash = prev_hash
		self.timestamp = str(datetime.datetime.utcnow())
		self.nonce = 0
	def convert(self):
		return {
			'prev_hash':self.prev_hash,
			'timestamp':self.timestamp,
			'nonce':self.nonce
		}

class Block:
	def __init__(self, transaction, prev_hash=0):
		self.header = Header(prev_hash)
		self.transaction = transaction
		self.hash = None
	def convert(self):
		return {
			'header':self.header.convert(),
			'transaction':self.transaction.convert(),
			'hash':self.hash
		}