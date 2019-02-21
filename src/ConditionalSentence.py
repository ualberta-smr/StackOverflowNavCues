from SOSentence import SOSentence

class ConditionalSentence(SOSentence):

	def __init__(self, sentence, question_id=None, answer_id=None, paragraph_index=None, sentence_pos=None, condition=None, tags=None, nfreqs=None, nouns=None, insightful=False):
		SOSentence.__init__(self, sentence, question_id, answer_id,paragraph_index, sentence_pos)
		self.condition = condition
		self.tags = tags
		self.nfreqs = nfreqs
		self.nouns = nouns
		self.insightful = insightful
		self.interrogative = False
		self.first_person = False
		self.unsure_phrase = False
		self.grammar_dependencies = False

	def set_grammar_dependencies(self, value):
		self.grammar_dependencies = value

	def set_unsure_phrase(self, value):
		self.unsure_phrase = value

	def set_interrogative(self, value):
		self.interrogative = value

	def set_first_person(self, value):
		self.first_person = value

	def set_condition(self, condition):
		self.condition = condition

	def set_tags(self, tags):
		self.tags = tags

	def set_nfreqs(self, nfreqs):
		self.nfreqs = nfreqs

	def set_nouns(self, nouns):
		self.nouns = nouns

	def set_insightful(self):
		self.insightful = True

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

	def is_insightful(self):
		return self.insightful

	def is_interrogative(self):
		return self.interrogative

	def is_first_person(self):
		return self.first_person

	def is_unsure_phrase(self):
		return self.is_unsure_phrase

	def has_grammar_dependencies(self):
		return self.grammar_dependencies

	def print(self, delimeter):
		print(self.insightful, self.question_id, self.answer_id, self.paragraph_index, self.sentence_pos, self.sentence.replace("-LRB-", "(").replace("-RRB-", ")"), self.condition, self.tags, self.nfreqs, self.nouns, self.interrogative, self.first_person, self.unsure_phrase, self.grammar_dependencies, sep=delimeter)




