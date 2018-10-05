class ConditionalSentence:

	def __init__(self, sentence, question_id, answer_id, paragraph_index=None, sentence_pos=None, condition=None, tags=None, nfreqs=None, nouns=None, baseline=True):
		self.sentence = sentence
		self.question_id = question_id
		self.answer_id = answer_id
		self.paragraph_index = paragraph_index
		self.sentence_pos = sentence_pos
		self.condition = condition
		self.tags = tags
		self.nfreqs = nfreqs
		self.nouns = nouns

	def set_sentence(self, sentence):
		self.sentence = sentence

	def set_condition(self, condition):
		self.condition = condition

	def set_tags(self, tags):
		self.tags = tags

	def set_nfreqs(self, nfreqs):
		self.nfreqs = nfreqs

	def set_nouns(self, nouns):
		self.nouns = nouns

	def set_not_baseline(self):
		self.baseline = False

	def get_sentence(self):
		return self.sentence

	def get_condition(self):
		return self.condition

	def get_tags(self):
		return self.tags

	def get_nfreqs(self):
		return self.nfreqs

	def get_nouns(self):
		return self.nouns

	def print(self, delimeter):
		print(self.baseline, self.question_id, self.answer_id, self.paragraph_index, self.sentence_index, self.sentence, self.condition, self.tags, self.nfreqs, self.nouns, sep='|')




