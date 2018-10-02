from stanfordcorenlp import StanfordCoreNLP
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP

class TextProcessor:


	def __init__(self, input, properties = {
        'annotators': 'pos,parse',
        'outputFormat': 'json'}):
		self.corenlp = pycorenlp_StanfordCoreNLP('http://localhost:9000')
		self.input = input
		self.corenlp_properties = properties
		self.annotations = None

	def annotate_input(self):
		self.annotations = self.corenlp.annotate(self.input, self.corenlp_properties)

	def get_sentences(self):
		return self.annotations['sentences']

	def get_num_sentences(self):
		return self.annotations['sentences'].size()

	def get_annotations(self):
		return self.annotations

	def get_sentence_text(self, sentence_index):
		sentence = self.annotations['sentences'][sentence_index]
		res = ""
		for word in sentence['tokens']:
			res += word['word'] + " "

		return res

	def get_condition_from_sentence(self, sentence_index):
		sentence = self.annotations['sentences'][sentence_index]

		parse_res = sentence['parse']
		split = parse_res.split("\n")
		condition = get_tree_from_parse_items(split)

		final = ""
		for item in condition:
    			if item:
        			final += item + " "

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

def main():
	test = "Test is a common name for test code. Use a different name if you want to signify real code"
	text_processor = TextProcessor(test)
	text_processor.annotate_input()
	print ("sentence 1: " , text_processor.get_sentence_text(0))
	print ("sentence 2: ",  text_processor.get_sentence_text(1))
	print ("condition 1: " , text_processor.get_condition_from_sentence(0))
	print ("condition 2: ", text_processor.get_condition_from_sentence(1))

if __name__ == "__main__":
	main()
