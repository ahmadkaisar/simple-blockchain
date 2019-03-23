from .requirement import *

class Value:
	def __init__(self, value, timestamp=str(datetime.datetime.utcnow())):
		self.value = str(value)
		self.timestamp = timestamp
	def convert(self):
		return {
			'value':self.value,
			'timestamp':self.timestamp
		}
	def hash(self):
		return hashlib.sha256(self.value.encode() + self.timestamp.encode()).hexdigest()

class Transaction:
	def __init__(self):
		self.transaction = []
	def add(self, value, timestamp=str(datetime.datetime.utcnow())):
		print('[*] add new transaction')
		self.transaction += [Value(value,timestamp)]
	def convert(self):
		res = []
		for transaction in self.transaction:
			res += [transaction.convert()]
		return res
	def hash(self):
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