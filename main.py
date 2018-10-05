from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence

def find_cond_sentences(questions):
	all_cond_sentences = list()
	print (len(questions['items']))
	for question in questions['items']:
		print ("looping over questions")
		for answer in question['answers']:
			print ("looping over answers")
			paragraphs = get_paragraphs(answer['body'])
			print ("got paragraphs")
			for paragraph_index, paragraph in enumerate(paragraphs):
				cond_sentences = get_cond_sentences(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
				print ("got ", len(cond_sentences), " cond sentences")
				all_cond_sentences.append(cond_sentences)

def main():
	SITE = StackAPI('stackoverflow')
	questions = SITE.fetch('questions', fromdate=datetime(2011,11,11), todate=datetime(2011,11,12), min=10, sort='votes', tagged='java', filter='!-*jbN-o8P3E5')
	print("boo")
	init_corenlp()
	print ("corenlp", corenlp)
	cond_sentences = find_cond_sentences(questions)
	if (cond_sentences):
		print ("found something")
	else:
		print ("cond sentences none")
	for cond_sentence in cond_sentences:
		cond_sentence.print()


if __name__ == "__main__":
	main()
