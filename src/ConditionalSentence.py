from SOSentence import SOSentence

class ConditionalSentence(SOSentence):

	def __init__(self, sentence, question_id=None, answer_id=None, paragraph_index=None, sentence_pos=None, condition=None, tags=None, nfreqs=None, nouns=None, conditional=False,interrogative=False):
		SOSentence.__init__(self, sentence, question_id, answer_id,paragraph_index, sentence_pos)
		self.condition = condition
		self.tags = tags
		self.nfreqs = nfreqs
		self.nouns = nouns
		self.conditional = conditional
		self.interrogative = interrogative


	def set_interrogative(self):
		self.interrogative = True

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

	def set_question_id(self, question_id):
		self.question_id = question_id

	def set_answer_id(self, answer_id):
		self.answer_id = answer_id

	def set_paragraph_index(self, paragraph_index):
		self.paragraph_index = paragraph_index

	def set_sentence_pos(self, sentence_pos):
		self.sentence_pos = sentence_pos

	def get_condition(self):
		return self.condition

	def get_tags(self):
		return self.tags

	def get_nfreqs(self):
		return self.nfreqs

	def get_nouns(self):
		return self.nouns

	def get_sentence(self):
		return self.sentence

	def is_conditional(self):
		return self.conditional

	def is_interrogative(self):
		return self.interrogative


	def print(self, delimeter):
		print("type of sentence in class: " + str(type(self.sentence)))
		print(self.conditional, self.question_id, self.answer_id, self.paragraph_index, self.sentence_pos, self.sentence.replace("-LRB-", "(").replace("-RRB-", ")"), self.condition, self.tags, self.nfreqs, self.nouns, sep=delimeter)




