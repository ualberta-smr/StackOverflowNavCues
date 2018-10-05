from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence

def find_cond_sentences(questions):
	all_cond_sentences = list()
	for question in questions['items']:
		for answer in question['answers']:
			paragraphs = get_paragraphs(answer['body'])
			for paragraph_index, paragraph in enumerate(paragraphs):
				cond_sentences = get_cond_sentences(paragraphs, question_id=question['id'], answer_id=answer['id'], paragraph_index=paragraph_index)
				all_cond_sentences.append(cond_sentences)

def main():
	SITE = StackAPI('stackoverflow')
	questions = SITE.fetch('questions', fromdate=datetime(2011,11,11), todate=datetime(2011,11,19), min=10, sort='votes', tagged='java', filter='!-*jbN-o8P3E5')
	cond_sentences = find_cond_sentences(questions)


if __name__ == "__main__":
	main()