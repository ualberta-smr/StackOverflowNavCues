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
			self.assertFalse(cond_sentence.has_valid_vb_dep())

	def test_verb_noun_dep(self):

		#should be tagged as a conditional insight
		#if related to verb, but verb has a dependency to a noun
		paragraph = "You should use Windows if you want features."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.has_valid_vb_dep())

	def test_if_no_dep(self):

		#should NOT be tagged as a conditional insight
		#the if not related to verb or noun
		paragraph = "You should use Windows if necessary."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.has_valid_vb_dep())
			self.assertFalse(cond_sentence.has_valid_noun_dep())

	def test_if_verb_dep_it(self):

		#should NOT be tagged as a conditional insight
		#if is related to a verb but that verb's subject is "it" (not noun) -- same as 1
		paragraph = "You should use Windows even if it fails."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.has_valid_vb_dep())

	def test_verb_phrase_dep(self):

		#should be tagged as a conditional insight
		#same as test_verb_noun_dep but there's a phrase invovled
		paragraph = "You should use Windows even if the response fails."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.has_valid_vb_dep())

	def test_if_dep_noun(self):

		#should be tagged as a conditional insight
		#the if has a direct dependency on a noun
		paragraph = "You should use Windows even if the intended effect is bluescreen."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.has_valid_noun_dep())

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
		paragraph = "I should mention that I didn't know that json is not managed in memory with temp tables (text/blob case)... I 'm not sure if it could lead to performance issues. I don't know if it's the best solution, but what I'm trying now is to just pass values as strings unformatted except for a decimal point, like so:"

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_unsure_phrase())

	def test_unsure_phrase2(self):
		paragraph = "Not sure if anyone still runs into this issue but I was able to address this in a dotnetcore console project (netcoreapp2 .0) via x. I'm not sure if this applies to some Java frameworks, too."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.is_unsure_phrase())

	def test_if_in_paren(self):
		paragraph = "(I did not choose this option because the `lambda' limits are lower than the Firehose limits, you can configure Firehose to write a file each 128Mb or 15 minutes, but if you associate this lambda function to Firehose, the lambda function will be executed every 3 mins or 5 MB, in my case I had the problem of generate a lot of little parquet files, as for each time that the lambda function is launched I generate at least 10 files). One quick workaround (if you have the luxury of code generation you can automate this): dummy text. There is a already an LINK for this in the postgres driver Github repository (even if the problem seems the be the serverside processing). You can use it for debugging your app on a local machine (if everything works in production)."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			print(cond_sentence.get_sentence())
			self.assertTrue(cond_sentence.is_if_in_paren())

	def test_wanted_if_you(self):
		paragraph = "Well, if you just need a single extra property, one simple approach is to parse your JSON to a CW, use CW to populate your class from the CW , and then use CW to pull in the extra property. Then you'll get the error because it 's not a string, it 's an object, and if you already have it in this form then there's no need to use CW. You can fix this problem if you are the owner of both domains. Alternatively if you want them to be represented as a set, and the elements are strings, you could put them in objects like CW."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertFalse(cond_sentence.has_unwanted_if_you())

	def test_unwanted_if_you(self):
		paragraph = "However, if you try with jQuery's CW and it's working, the reason is probably because of jQuery using CW instead of CW."

		for cond_sentence in get_cond_sentences_from_para(paragraph, None, None, None):
			self.assertTrue(cond_sentence.has_unwanted_if_you())

if __name__ == "__main__":
	unittest.main()