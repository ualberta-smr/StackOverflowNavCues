import ConditionalSentence
from stanfordcorenlp import StanfordCoreNLP
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP


corenlp_properties={'annotators': 'pos,parse',
        'outputFormat': 'json'}

corenlp = None

def set_core_nlp_properties(properties):
	corenlp_properties=properties

def init_corenlp():
	corenlp = pycorenlp_StanfordCoreNLP('http://localhost:9000')

def get_cond_sentences(paragraph, question_id, answer_id, paragraph_index):
	cond_sentences = list()
	annotations = corenlp.annotate(paragraph, corenlp_properties)
	for sentence_index in annotations['sentences'].size():
		sentence_text = get_sentence_text(sentences[sentence_index])
		if " if" in sentence_text.lower():
			ConditionalSentence cond_sentence(sentence=sentence_text, question_id=question_id, answer_id=answer_id, paragraph_index=paragraph_index, sentence_index=sentence_index)
            cond_sentence.set_condition(get_condition(sentence))
            cond_sentence.set_nfreqs(get_non_func(condition))
            nouns_in_cond = list(set(get_nouns(sentence, condition) + get_regex_nouns(sentence_text)))
            cond_sentence.set_nouns(nouns_in_cond)
            tags_in_cond = get_tags(nouns_in_cond)

            #Our criteria for a "useful" conditional sentence is that it contains one of the SO tags in its condition
            if (len(tags_in_cond) != 0 ):
            	cond_sentence.set_not_baseline()
            	cond_sentence.set_tags(tags_in_cond))

            cond_sentence.append(cond_sentence)

def get_tags(word_list):
    res = []
    for word in word_list:
        if word.lower() in TAGS_LIST:
            res.append(word.lower())

    return res

def get_sentence_text(sentence):
	res = ""
	for word in sentence['tokens']:
		res += word['word'] + " "

	return res


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

def get_nouns(sentence, condition):
    res = []
    words = set(re.sub("[^\w]", " ",  condition).split())
    
    for token in sentence["tokens"]:
        if token["originalText"].lower() in words and token["pos"] in NOUN_IDENTIFIERS:
            res.append(token["originalText"])

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
