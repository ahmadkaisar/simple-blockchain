from .requirement import *

class Value:
	def __init__(self, fromAddress=b'', toAddress=b'', value=b''):
		self.fromAddress = str(fromAddress)
		self.toAddress = str(toAddress)
		self.value = str(value)
	def convert(self):
		return {
			'fromAddress':self.fromAddress,
			'toAddress':self.toAddress,
			'value':self.value
		}
	def decodeJson(self, data):
		self.fromAddress = data['fromAddress']
		self.toAddress = data['toAddress']
		self.value = data['value']
	def hash(self):
		return hashlib.sha256(self.fromAddress.encode() + self.toAddress.encode() + self.value.encode()).hexdigest()

class Transaction:
	def __init__(self, value=Value(), timestamp=str(datetime.datetime.utcnow())):
		self.value = value
		self.timestamp = timestamp
	def convert(self):
		return {
			'transaction':self.value.convert(),
			'timestamp':self.timestamp
		}
	def decodeJson(self, data):
		self.value.decodeJson(data['transaction'])
		self.timestamp = data['timestamp']
	def hash(self):
		return hashlib.sha256(self.timestamp.encode() + self.value.hash().encode()).hexdigest()

class Transactions:
	def __init__(self):
		self.transaction = list()
	def add(self, value, timestamp=str(datetime.datetime.utcnow())):
		print('[*] add new transaction')
		self.transaction.append(Transaction(value,timestamp))
	def convert(self):
		res = []
		for transaction in self.transaction:
			res += [transaction.convert()]
		return res
	def decodeJson(self, data):
		self.transaction = list()
		for transaction in data:
			temp_transaction = Transaction()
			temp_transaction.decodeJson(transaction)
			self.transaction.append(temp_transaction)
	def hash(self):
		if len(self.transaction) < 1:
			return ''
		thash = [x.hash() for x in self.transaction]
		thash, self.transaction = zip(*sorted(zip(thash, self.transaction)))
		thash = list(thash)
		while float(int(math.log2(len(thash)))) != math.log2(len(thash)):
			thash += [thash[-1]]
		while len(thash) > 1:
			temp = []
			for i in range(0, len(thash), 2):
				temp += [hashlib.sha256(thash[i].encode() + thash[i + 1].encode()).hexdigest()]
			thash = temp
		return thash[0]