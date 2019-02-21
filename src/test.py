from ConditionalSentence import ConditionalSentence
from corenlp_helper import *
import unittest

class TestConditionalSentences(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		init_corenlp()

	def test_verb_no_dep(self):

		#should NOT be tagged as a conditional insight
		#if related to verb, but verb has no dependencies to a noun (any noun... NN*)
		paragraph = "You should use Windows if you want."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.is_conditional())

	def test_verb_noun_dep(self):

		#should be tagged as a conditional insight
		#if related to verb, but verb has a dependency to a noun
		paragraph = "You should use Windows if you want features."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_conditional())

	def test_if_no_dep(self):

		#should NOT be tagged as a conditional insight
		#the if not related to verb or noun
		paragraph = "You should use Windows if necessary."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.is_conditional())

	def test_if_verb_dep_it(self):

		#should NOT be tagged as a conditional insight
		#if is related to a verb but that verb's subject is "it" (not noun) -- same as 1
		paragraph = "You should use Windows even if it fails."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.is_conditional())

	def test_verb_phrase_dep(self):

		#should be tagged as a conditional insight
		#same as test_verb_noun_dep but there's a phrase invovled
		paragraph = "You should use Windows even if the response fails."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_conditional())

	def test_if_dep_noun(self):

		#should be tagged as a conditional insight
		#the if has a direct dependency on a noun
		paragraph = "You should use Windows even if the intended effect is bluescreen."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_conditional())

	def test_interrogative_sentence(self):
		paragraph = "Now, if we issue the exact same PATCH request as above, what happens?"

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_interrogative())

	def test_not_interrogative_sentence(self):
		paragraph = "I even used Postman to check if I had the correct routes or endpoint ."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.is_interrogative())

	def test_first_person(self):
		paragraph = "I even used Postman to check if I had the correct routes or endpoint."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_first_person())

	def test_not_first_person(self):
		paragraph = "I should mention that I didn't know that json is not managed in memory with temp tables (text/blob case)... I 'm not sure if it could lead to performance issues."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.is_first_person())

	def test_unsure_phrase(self):
		paragraph = "I should mention that I didn't know that json is not managed in memory with temp tables (text/blob case)... I 'm not sure if it could lead to performance issues."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_unsure_phrase())

if __name__ == "__main__":
	unittest.main()