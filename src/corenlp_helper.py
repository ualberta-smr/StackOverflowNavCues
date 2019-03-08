from ConditionalSentence import ConditionalSentence
from SOSentence import SOSentence
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP
import re
from regex import REGEX_LIST
from tags import load_tags, TAGS_LIST, QUALITY_WORDS
import sys
from nltk.stem.porter import *

MODAL_VERBS = {
    "shall", 
    "should",
    "will",
    "must", 
    "would", 
    "can", 
    "might",
    "could",
    "may",
}

NOUN_IDENTIFIERS = {'NN', 'NNS', 'NNP', 'NNPS'}

VERB_IDENTIFIERS = {'VBP', 'VBZ'}

#General CoreNLP Setup
corenlp_properties={'annotators': 'pos,parse', 'outputFormat': 'json', 'timeout': 30000}

corenlp = None

stemmer = PorterStemmer()

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

def get_sentence_text_lemmatized(sentence):
	res = ""
	for word in sentence['tokens']:
		res += word['lemma'] + " "

	return res

def get_index(tree):
	index = 0
	for item in tree:
		#there are these extra spaces in the tree. We basically want to get the index of the
		#first subtree of the if so we want to ignore these spaces and know what the index of
		#that subtree is
		if item == " ": 
			index += 1
		else:
			return index


def get_conditional_tree(parse_items):
	index = None
	res = []
	for item in parse_items:
		#this check signifies that we are in an if clause
		# An example of a parse tree would look like this
		# (ROOT
		# (S
		#   (SBAR (IN If)
		#     (S
		#       (ADVP (RB instead))
		#       (NP (DT the) (NN client))
		#       (VP (VBZ uses)
		#         (NP (DT a) (NN PUT) (NN request))
		#         (S
		#           (VP (TO to)
		#             (VP (VB correct)
		#               (NP (DT the) (NN email)))))
		#         (, ,)

		if "in if" in item.lower(): 
			index = get_index(item)
		else:
			#if we have already seen an if condition, then we will have an index
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

def is_first_person_condition(sentence):
	tokens = sentence['tokens']

	for token_index, token in enumerate(tokens):
		if token['word'] == "if":
			if (token_index <= len(tokens) - 2 and tokens[token_index + 1]['word'].lower() == "i"):
				return True

	return False

def is_interrogative_sentence(sentence):
	#simply check if it ends with a question mark
	tokens = sentence["tokens"]
	if (tokens[len(tokens) - 1]['word'] == "?"):
		return True

	return False

def contains_unsure_phrases(sentence_text):
	return "not sure" in sentence_text or "don't know" in sentence_text or "don ' t know" in sentence_text or "don 't know" in sentence_text

def verb_has_dep_noun(enhancedDependencies, verb_token_index, tokens):
	for dependency in enhancedDependencies:
		if dependency['governor'] == verb_token_index:
			dependent_index = int(dependency['dependent'])
			dependent_pos = tokens[dependent_index - 1]['pos']
			if (dependent_pos in NOUN_IDENTIFIERS):
				return True

	return False

def check_relevant_grammar_dependencies(sentence, cond_sentence):

	tokens = sentence["tokens"]
	enhanced_dependencies = sentence['enhancedDependencies']
	is_relevant_condition = False
	for dependency in enhanced_dependencies:
		if dependency['dependentGloss'] == "if":
			governor_token_index = int(dependency['governor'])
			governor_pos = tokens[governor_token_index - 1]['pos']
			if governor_pos in VERB_IDENTIFIERS:
				cond_sentence.set_valid_vb_dep(verb_has_dep_noun(enhanced_dependencies, governor_token_index, tokens))
			elif governor_pos in NOUN_IDENTIFIERS:
				cond_sentence.set_valid_noun_dep(True)


def condition_contains_so_tag(cond_sentence, nouns_in_cond):
	#One criteria for a "useful" conditional sentence is that it contains one of the SO tags in its condition
	tags_in_cond = get_tags(nouns_in_cond)
	if (len(tags_in_cond) != 0):
		cond_sentence.set_tags(tags_in_cond)
		return True
	else:
		return False
		


def build_cond_sentence(sentence):
	try:
		sentence_text = get_sentence_text(sentence)

		if " if" in sentence_text.lower():
			#initialize conditional sentence with basic info
			cond_sentence = ConditionalSentence(sentence=sentence_text)

			#get information about condition, nfrs etc
			condition = get_condition_from_sentence(sentence)
			cond_sentence.set_condition(condition)
			cond_sentence.set_nfreqs(get_non_func(condition))
			nouns_in_cond = list(set(get_nouns(sentence, condition) + get_regex_code_elem(sentence_text)))
			cond_sentence.set_nouns(nouns_in_cond)

			#check all our criteria for a conditional sentence being insightful
			check_relevant_grammar_dependencies(sentence, cond_sentence)

			#cond_sentence.set_grammar_dependencies(True)

			if (condition_contains_so_tag(cond_sentence,nouns_in_cond)):
				cond_sentence.set_insightful(True)
				cond_sentence.set_so_tag(True)

			if (is_interrogative_sentence(sentence)):
				cond_sentence.set_interrogative(True)
				 #filter out sentences that are interrogative, even if they fulfilled prev criteria
				cond_sentence.set_insightful(False)

			if (is_first_person_condition(sentence)):
				cond_sentence.set_first_person(True)
				#filter out sentences that have first person in their condition, even if they fulfilled prev criteria
				cond_sentence.set_insightful(False)

			if (contains_unsure_phrases(sentence)):
				cond_sentence.set_unsure_phrase(True)
				#filter out sentences that have unsure phrases, even if they fulfilled prev criteria
				cond_sentence.set_insightful(False)

			return cond_sentence

	except Exception as e:
		print(e)
		traceback.print_exc()
		print("Failed to process sentence: " + sentence_text)

	return None

## @Christoph: this is where you would want to play with things
def get_cond_sentences_from_para(paragraph, q_id, answ_id, parag_index):
	cond_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)

	try:
		for sent_index, sentence in enumerate(annotations['sentences']):
			try:
				cond_sentence = build_cond_sentence(sentence)
				if (cond_sentence is not None):
					cond_sentence.set_question_id(q_id)
					cond_sentence.set_answer_id(answ_id)
					cond_sentence.set_sentence_pos(sent_index)
					cond_sentence.set_paragraph_index(parag_index)

					cond_sentences.append(cond_sentence)
			except Exception as e: 
				print(e)
				traceback.print_exc()
				print("Failed to enumerate sentence " + sent_index + "(" + sentence + ") in para:" + str(q_id) + "," + str(answ_id) + "," + str(parag_index) + ": " + paragraph, file=sys.stderr)
	except Exception as e: 
			print(e)
			traceback.print_exc()
			print("Failed to enumerate paragraph " + str(q_id) + "," + str(answ_id) + "," + str(parag_index) + ": " + paragraph, file=sys.stderr)


	return cond_sentences


def get_condition_from_sentence(sentence):
	parse_res = sentence['parse']
	#print (parse_res)
	split = parse_res.split("\n")
	conditional_tree = get_conditional_tree(split)

	condition = ""
	for item in conditional_tree:
			if item:
				condition += item + " "

	if (len(condition) == 0):
		return None
	else:
		return condition

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
		if stemmer.stem(word).lower() in TAGS_LIST:
			res.append(word.lower())

	return res


def get_nouns(sentence, condition):
	res = []
	words = set(re.sub("[^\w]", " ",  str(condition)).split())

	for token in sentence["tokens"]:
		#print ("token: " + str(token))
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
	corenlp_properties={'annotators': 'pos,parse,lemma', 'outputFormat': 'json'}
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	try:
		for sent_index, sentence in enumerate(annotations['sentences']):
			sentence_text = get_sentence_text_lemmatized(sentence)
			if check_word_pattern(replace_regex_code_elem(sentence_text), patterns):
				so_sentence = SOSentence(sentence=sentence_text, question_id=q_id, answer_id=answ_id, sentence_pos=sent_index, paragraph_index=parag_index)
				word_pattern_sentences.append(so_sentence)
	except:

		print("Failed to enumerate sentences in para:" + str(q_id) + "," + str(answ_id) + "," + str(parag_index) + ": " + paragraph, file=sys.stderr)
	return word_pattern_sentences


## Baseline 2: LexRank
# TODO

def get_all_paragraph_sentences(paragraph):
	corenlp_properties={'annotators': 'pos,parse,lemma', 'outputFormat': 'json'}
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	all_sentences = list()

	try:
		for sentence in annotations['sentences']:
			sentence_text = get_sentence_text_lemmatized(sentence)
			all_sentences.append(sentence_text)
	except:
		print("Failed to process paragraph:" + paragraph, file=sys.stderr)
	
	return all_sentences

def get_all_thread_sentences(paragraph, q_id, answ_id, parag_index):
	word_pattern_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	for sent_index, sentence in enumerate(annotations['sentences']):
		sentence_text = get_sentence_text(sentence)
		if check_word_pattern(replace_regex_code_elem(sentence_text), patterns):
			so_sentence = SOSentence(sentence=sentence_text, question_id=q_id, answer_id=answ_id, sentence_pos=sent_index, paragraph_index=parag_index)
			word_pattern_sentences.append(so_sentence)

	return word_pattern_sentences

