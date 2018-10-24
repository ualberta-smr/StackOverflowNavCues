from ConditionalSentence import ConditionalSentence
from SOSentence import SOSentence
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP
import re
from regex import REGEX_LIST
from tags import load_tags, TAGS_LIST, QUALITY_WORDS, NOUN_IDENTIFIERS
import sys

#General CoreNLP Setup
corenlp_properties={'annotators': 'pos,parse', 'outputFormat': 'json'}

corenlp = None

def set_core_nlp_properties(properties):
	global corenlp_properties
	corenlp_properties=properties

def init_corenlp():
	global corenlp
	corenlp=pycorenlp_StanfordCoreNLP('http://localhost:9000')


#General helper functions to process corenlp annotation results
def get_sentence_text(sentence):
	res = ""
	for word in sentence['tokens']:
		res += word['word'] + " "

	return res


def get_index(snippet):
	count = 0
	for item in snippet:
		if item == " ":
			count += 1
		else:
			return count


def get_tree_from_parse_items(items):
	index = None
	res = []
	for item in items:
		if "in if" in item.lower():
			index = get_index(item)
		else:
			if index:
				if "(, ,)" in item:
					return res

				if get_index(item) >= index:
					res.append(get_word(item))
				elif get_index(item) < index:
								return res
			else:
				continue

	return res

def get_word(item):
	res = ""
	for char in item[::-1]:
		if char == " ":
			return res
		elif char == ")":
			continue
		elif char == "(":
			return None
		else:
			res = char + res

	return res

## Conditional Sentences
def get_cond_sentences(paragraph, q_id, answ_id, parag_index):
	cond_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	try:
		for sent_index, sentence in enumerate(annotations['sentences']):
			sentence_text = get_sentence_text(sentence)
			if " if" in sentence_text.lower():
				#initialize conditional sentence with basic info
				cond_sentence = ConditionalSentence(sentence=sentence_text, question_id=q_id, answer_id=answ_id, sentence_pos=sent_index, paragraph_index=parag_index)

				#get information about condition, nfrs etc
				condition = get_condition_from_sentence(sentence)
				cond_sentence.set_condition(condition)
				cond_sentence.set_nfreqs(get_non_func(condition))
				nouns_in_cond = list(set(get_nouns(sentence, condition) + get_regex_code_elem(sentence_text)))
				cond_sentence.set_nouns(nouns_in_cond)
				tags_in_cond = get_tags(nouns_in_cond)

				#Our criteria for a "useful" conditional sentence is that it contains one of the SO tags in its condition
				if (len(tags_in_cond) != 0 ):
					cond_sentence.set_conditional()
					cond_sentence.set_tags(tags_in_cond)

				cond_sentences.append(cond_sentence)
	except:
		print("Failed to enumerate sentences in para:" + str(q_id) + "," + str(answ_id) + "," + str(parag_index) + ": " + paragraph, file=sys.stderr)

	return cond_sentences


def get_condition_from_sentence(sentence):
	parse_res = sentence['parse']
	split = parse_res.split("\n")
	condition = get_tree_from_parse_items(split)

	final = ""
	for item in condition:
			if item:
				final += item + " "

	if (len(final) == 0):
		return None
	else:
		return final

def get_non_func(string):
	res = []

	if string:
		for word in re.sub("[^\w]", " ",  str(string)).split():
			if word.lower() in QUALITY_WORDS:
				res.append(word)
	
	return res

def get_regex_code_elem(sentence_text):
	result = []
	for pattern in REGEX_LIST:
		for word in sentence_text.split():
			if re.match(pattern, word):
				result.append(word)

	return result

def get_tags(word_list):
	res = []
	for word in word_list:
		if word.lower() in TAGS_LIST:
			res.append(word.lower())

	return res


def get_nouns(sentence, condition):
	res = []
	words = set(re.sub("[^\w]", " ",  str(condition)).split())

	for token in sentence["tokens"]:
		if token["originalText"].lower() in words and token["pos"] in NOUN_IDENTIFIERS:
			res.append(token["originalText"])

	return res


## Baseline 1: Word Patterns

def replace_regex_code_elem(sentence_text):
	new_sentence_text = sentence_text
	for pattern in REGEX_LIST:
		new_sentence_text = re.sub(pattern, "CW", new_sentence_text)

	return new_sentence_text

def check_word_pattern(sentence_text, patterns):
    found_match = False

    for pattern in patterns:
        all_found = True
        for item in pattern:
            # if item == "CW":
            #     continue
            if not item in sentence_text:
                all_found = False
                break

        if all_found:
            return True

def get_word_pattern_sentences(patterns, paragraph, q_id, answ_id, parag_index):
	word_pattern_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	try:
		for sent_index, sentence in enumerate(annotations['sentences']):
			sentence_text = get_sentence_text(sentence)
			if check_word_pattern(replace_regex_code_elem(sentence_text), patterns):
				so_sentence = SOSentence(sentence=sentence_text, question_id=q_id, answer_id=answ_id, sentence_pos=sent_index, paragraph_index=parag_index)
				word_pattern_sentences.append(so_sentence)
	except:
		print("Failed to enumerate sentences in para:" + q_id + "," + answ_id + "," + parag_index + ": " + paragraph, file=sys.stderr)
	return word_pattern_sentences


## Baseline 2: LexRank
# TODO
def get_stemmed_para_sentences(paragraph, q_id, answ_id, parag_index):
	word_pattern_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	for sent_index, sentence in enumerate(annotations['sentences']):
		sentence_text = get_sentence_text(sentence)
		if check_word_pattern(replace_regex_code_elem(sentence_text), patterns):
			so_sentence = SOSentence(sentence=sentence_text, question_id=q_id, answer_id=answ_id, sentence_pos=sent_index, paragraph_index=parag_index)
			word_pattern_sentences.append(so_sentence)

	return word_pattern_sentences

