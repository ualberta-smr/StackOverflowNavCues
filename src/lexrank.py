from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags
from lexrank import STOPWORDS, LexRank
from path import Path



def find_interesting_sentences(questions):
	patterns = read_patterns_file()
	all_interesting_sentences = list()

	items = questions.get('items')

	if items is not None:
		for question in items:
			answers = question.get('answers')
			#we want to consider threads that have at least 2 answers
			if answers is not None and len(answers) >= 2:
				for answer in answers:
					paragraphs = get_paragraphs(answer['body'])
					if paragraphs is not None:
						for paragraph_index, paragraph in enumerate(paragraphs):

							#get conditional sentences (our technique and also includes just sentences with "if")
							cond_sentences = get_cond_sentences(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
							all_interesting_sentences.extend(cond_sentences)

							#get baseline 1 sentences based on Martin's patterns
							word_pattern_sentences = get_word_pattern_sentences(patterns,paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
							all_interesting_sentences.extend(word_pattern_sentences)

	return all_interesting_sentences

def read_question_ids():
    question_ids = []
    with open("question_ids.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            question_ids.append([item.strip() for item in items])

    return question_ids

def extract_doc_from_thread(question, path="./tmp"):
	output_file = open(path + str(question['question_id']) + ".txt", "w")

	answers = question.get('answers')

	for answer in answers:
		paragraphs = get_paragraphs(answer['body'])
		if paragraphs is not None:
			print(paragraph, file=output_file)


def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	question_ids = read_question_ids()

	#get all threads for the ids we are interested in
	questions = SITE.fetch('/questions/{ids}', ids=question_ids, filter='!-*jbN-o8P3E5')
	
	#for each thread, write out all text of that thread in a corresponding document file first
	items = questions.get('items')

	if items is not None:
		for question in items:
			extract_doc_from_thread(question)
	
	documents_dir = Path('./tmp')
	documents = []

	for file_path in documents_dir.files('*.txt'):
    	with file_path.open(mode='rt', encoding='utf-8') as fp:
        	documents.append(fp.readlines())

	lxr = LexRank(documents, stopwords=STOPWORDS['en'])
	print(lxr)

if __name__ == "__main__":
	main()
