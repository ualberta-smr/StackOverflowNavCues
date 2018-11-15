from ConditionalSentence import ConditionalSentence
from SOSentence import SOSentence
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP
import re
from regex import REGEX_LIST
from tags import load_tags, TAGS_LIST, QUALITY_WORDS, NOUN_IDENTIFIERS
import sys

corenlp_properties={'annotators': 'pos,parse,tokenize,ssplit,lemma,tokensregex', 'outputFormat': 'json', 'tokensregex.rules':'basic_ner.rules'}

def set_core_nlp_properties(properties):
	global corenlp_properties
	corenlp_properties=properties

def init_corenlp():
	global corenlp
	corenlp=pycorenlp_StanfordCoreNLP('http://localhost:9000')

def get_sentence_text(sentence):
	res = ""
	for word in sentence['tokens']:
		res += word['word'] + " "

	return res

def main():
	init_corenlp()
	
	try:
		annotations = corenlp.annotate("She has worked at Miller Corp. for 5 years. There will be a big announcement by Apple Inc today at 5:00pm. He works for apple inc in cupertino.", corenlp_properties)
		print(annotations)
		for sentence in annotations['sentences']:
			print("========")
			print(sentence)
			sentence_text = get_sentence_text(sentence)
	except Exception as e: print(e)
		
if __name__ == "__main__":
	main()
