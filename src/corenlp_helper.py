from ConditionalSentence import ConditionalSentence
from SOSentence import SOSentence
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP
import re
from regex import REGEX_LIST
from tags import load_tags, TAGS_LIST, QUALITY_WORDS
import sys
from nltk.stem.porter import *
import traceback

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
	punctuation = [".", ",", ":", "'"]
	sentence_len = len(sentence['tokens'])
	for index, token in enumerate(sentence['tokens']):
		curr_word = token['word']
		next_word = sentence['tokens'][index + 1]['word'] if index + 1 < sentence_len else None
		res += token['word'] 
		if next_word is not None and (next_word not in punctuation and not next_word.startswith("'")):
			res += " "

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

#we want to ignore conditions that are in parentheses (if x..)
def is_if_in_paren(sentence_text):
	#check if the if sentence is in parentheses
	sentence_text_stripped = sentence_text.strip().lower()
	return "-lrb- if" in sentence_text_stripped or sentence_text_stripped.startswith("-lrb-") or sentence_text_stripped.startswith("(") or "(if" in sentence_text.strip() or "( if" in sentence_text.strip()

#ignore sentences which contain "if you" (except exceptions in the next point)
# keep sentences where "if you" is followed by: are, have, want, or need (i.e., if you are, if you have, if you want, if you need)
# keep sentence where the "if" is not followed by "you".
def contains_unwanted_if_you(sentence, sentence_text):
	sentence_text_lower = sentence_text.lower()
	approved_verbs = ['have', 'are', 'want', 'need']
	if "if you" in sentence_text_lower:
		tokens = sentence["tokens"]
		enhanced_dependencies = sentence['enhancedDependencies']
		
		for dependency in enhanced_dependencies:
			#risk of this not working correctly if the you we are interested in is not the first you
			if dependency['dependentGloss'] == "you":
				governor = dependency['governorGloss']
				governor_token_index = int(dependency['governor'])
				governor_pos = tokens[governor_token_index - 1]['pos']
				if governor_pos in VERB_IDENTIFIERS and governor not in approved_verbs:
					return True
	
	return False


def contains_unsure_phrases(sentence_text):
	sentence_text_lower = sentence_text.lower()
	return "not sure" in sentence_text_lower or "don't know" in sentence_text_lower or "do n't know" in sentence_text_lower or "don 't know" in sentence_text_lower

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

			#set the value for all the factors/features we check for
			check_relevant_grammar_dependencies(sentence, cond_sentence)

			if (cond_sentence.has_valid_vb_dep() or cond_sentence.has_valid_noun_dep())
				cond_sentence.set_grammar_dependencies(True)
			cond_sentence.set_so_tag(condition_contains_so_tag(cond_sentence,nouns_in_cond))
			cond_sentence.set_interrogative(is_interrogative_sentence(sentence))
			cond_sentence.set_first_person(is_first_person_condition(sentence))
			cond_sentence.set_unsure_phrase(contains_unsure_phrases(sentence_text))
			cond_sentence.set_if_in_paren(is_if_in_paren(str(sentence_text)))
			cond_sentence.set_unwanted_if_you(contains_unwanted_if_you(sentence, sentence_text))


			#check combination of heuristics to set as insightful
			##### Heuristics:
			#########Heuristic 1: If any noun in the conditional phrase is a SO tag, then this is a "useful" sentence
			#########Heuristic 2: Grammatical Relationships
			#############Heuristic 2.1: The "if" must be related to a verb and that verb must have a dependency on a noun
			#############Heuristic 2.2: OR the "if" must be related to a noun
			#########Herustic 3: Conditional sentences that are actually question phrases are not "useful"
			#########Heursitc 4: If there is a first person reference "I" after the "if", this sentence is not "useful"
			#########Heurstic 5: Sentences containing uncertainty with phrases like "I don't know" or "I'm not sure" are not useful
			#########Heuristic 6: ignore if sentences in parentheses
			#########Heuristic 7: ignore sentences with "if you" unless it's if you have, if you want, if you are, if you need

			#first, check basic heuristics: heuristic 1 + heuristic 2
			if cond_sentence.has_so_tag() and cond_sentence.has_grammar_dependencies()):
				cond_sentence.set_insightful(True)

				#then start filtering out "bad" sentences
				if cond_sentence.is_interrogative():
					cond_sentence.set_insightful(False)
					return cond_sentence #no need to check for more

				if cond_sentence.is_first_person():
					cond_sentence.set_insightful(False)
					return cond_sentence #no need to check for more

				if cond_sentence.is_unsure_phrase():
					cond_sentence.set_insightful(False)
					return cond_sentence #no need to check for more

				if cond_sentence.is_if_in_paren():
					cond_sentence.set_insightful(False)
					return cond_sentence #no need to check for more

				if cond_sentence.has_unwanted_if_you():
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
	processed_sentences = 0
	failed_sentences = 0

	try:
		for sent_index, sentence in enumerate(annotations['sentences']):
			processed_sentences += 1
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
				failed_sentences += 1
				print("Failed to enumerate sentence " + sent_index + "(" + sentence + ") in para:" + str(q_id) + "," + str(answ_id) + "," + str(parag_index) + ": " + paragraph, file=sys.stderr)
	except Exception as e: 
			print(e)
			traceback.print_exc()
			print("Failed to enumerate paragraph " + str(q_id) + "," + str(answ_id) + "," + str(parag_index) + ": " + paragraph, file=sys.stderr)
			return None, 0, 0


	return cond_sentences, processed_sentences, failed_sentences


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

## not used
def get_all_thread_sentences(paragraph, q_id, answ_id, parag_index):
	word_pattern_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	for sent_index, sentence in enumerate(annotations['sentences']):
		sentence_text = get_sentence_text(sentence)
		if check_word_pattern(replace_regex_code_elem(sentence_text), patterns):
			so_sentence = SOSentence(sentence=sentence_text, question_id=q_id, answer_id=answ_id, sentence_pos=sent_index, paragraph_index=parag_index)
			word_pattern_sentences.append(so_sentence)

	return word_pattern_sentences

