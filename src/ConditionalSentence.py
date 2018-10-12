from SOSentence import SOSentence

class ConditionalSentence(SOSentence):

	def __init__(self, sentence, question_id, answer_id, paragraph_index=None, sentence_pos=None, condition=None, tags=None, nfreqs=None, nouns=None, conditional=False):
		SOSentence.__init__(self, sentence, question_id, answer_id,paragraph_index, sentence_pos)
		self.condition = condition
		self.tags = tags
		self.nfreqs = nfreqs
		self.nouns = nouns
		self.conditional = conditional


	def set_condition(self, condition):
		self.condition = condition

	def set_tags(self, tags):
		self.tags = tags

	def set_nfreqs(self, nfreqs):
		self.nfreqs = nfreqs

	def set_nouns(self, nouns):
		self.nouns = nouns

	def set_conditional(self):
		self.conditional = True

	def get_condition(self):
		return self.condition

	def get_tags(self):
		return self.tags

	def get_nfreqs(self):
		return self.nfreqs

	def get_nouns(self):
		return self.nouns

	def print(self, delimeter):
		print(self.conditional, self.question_id, self.answer_id, self.paragraph_index, self.sentence_pos, self.sentence.replace("-LRB-", "(").replace("-RRB-", ")"), self.condition, self.tags, self.nfreqs, self.nouns, sep=delimeter)




