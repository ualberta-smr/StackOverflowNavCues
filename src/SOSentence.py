class SOSentence:

	def __init__(self, sentence, question_id, answer_id, paragraph_index=None, sentence_pos=None):
		self.sentence = sentence
		self.question_id = question_id
		self.answer_id = answer_id
		self.paragraph_index = paragraph_index
		self.sentence_pos = sentence_pos

	def set_sentence(self, sentence):
		self.sentence = sentence

	def get_sentence(self):
		return self.sentence

	def print(self, sen_type, delimeter):
		print(sen_type, self.question_id, self.answer_id, self.paragraph_index, self.sentence_pos, self.sentence.replace("-LRB-", "(").replace("-RRB-", ")"),sep=delimeter)




