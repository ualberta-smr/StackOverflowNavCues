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

	def annotate_input():
		self.annotations = corenlp.annotate(all_text, corenlp_properties)

	def get_sentences():
		return self.annotations['sentences']

	def get_annotations():
		return annotations

	def main():
		test = "Test is a common name for test code. Use a different name if you want to signify real code"
		TextProcessor text_processor(test)
		text_processor.annotate_input()
		print (text_processor.get_annotations)

	if __name__== "__main__:
		main()