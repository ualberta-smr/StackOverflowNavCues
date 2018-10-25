from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags
from path import Path


def read_question_ids():
    question_ids = []
    with open("question_ids.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            question_ids.append([item.strip() for item in items])

    return question_ids

def extract_paratxt_from_thread(question):
	thread_sentences = list()
	answers = question.get('answers')

	with open('./lexrank/' + str(question['question_id']) + '.txt', 'w') as file:    
		for answer in answers:
			paragraphs = get_paragraphs(answer['body'])
			if paragraphs is not None:
				if paragraphs is not None:
					for paragraph in paragraphs:
						for sentence in get_all_paragraph_sentences(paragraph):
							file.write(sentence)
						file.write("\n\n")

		file.close()


def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	question_ids = read_question_ids()

	#get all threads for the ids we are interested in
	questions = SITE.fetch('/questions/{ids}', ids=question_ids, filter='!-*jbN-o8P3E5')
	
	items = questions.get('items')

	if items is not None:
		for question in items:
			extract_paratxt_from_thread(question)

if __name__ == "__main__":
	main()
