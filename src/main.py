from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags


def find_interesting_sentences(questions):
	patterns = read_patterns_file()
	all_interesting_sentences = list()

	items = questions.get('items')

	if items is not None:
		for question in items:
			answers = question.get('answers')
			all_answer_sentences = list()
			num_cond_sentences = 0
			num_b1_sentences = 0
			#we want to consider threads that have at least 2 answers
			if answers is not None and len(answers) >= 2:
				for answer in answers:
					paragraphs = get_paragraphs(answer['body'])
					if paragraphs is not None:
						for paragraph_index, paragraph in enumerate(paragraphs):

							#get conditional sentences (our technique and also includes just sentences with "if")
							cond_sentences = get_cond_sentences(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
							all_interesting_sentences.extend(cond_sentences)
							num_cond_sentences += len(cond_sentences)

							#get baseline 1 sentences based on Martin's patterns
							word_pattern_sentences = get_word_pattern_sentences(patterns,paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
							all_interesting_sentences.extend(word_pattern_sentences)
							num_b1_sentences += len(word_pattern_sentences)

	return all_interesting_sentences

def read_patterns_file():
    patterns = []
    with open("patterns.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            patterns.append([item.strip() for item in items])

    return patterns

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
			for paragraph in paragraphs:
				print(paragraph, file=output_file)

	output_file.close()

def extract_paratxt_from_thread(question):
	thread_sentences = list()
	answers = question.get('answers')

	for answer in answers:
		paragraphs = get_paragraphs(answer['body'])
		if paragraphs is not None:
			if paragraphs is not None:
				for paragraph in paragraphs:
					thread_sentences.extend(get_all_paragraph_sentences(paragraph))

	output_file.close()

def get_lexrank_summaries():
	SITE = StackAPI('stackoverflow')
	question_ids = read_question_ids()

	#get all threads for the ids we are interested in
	questions = SITE.fetch('/questions/{ids}', ids=question_ids, filter='!-*jbN-o8P3E5')
	
				#get lexrank summary

			#to be fair, we will do the summary size based on the maximum number of sentences identified by the other
			#techniques
			summary_size = max(len(cond_sentences), len(word_pattern_sentences))
			#get lexrank summary

	print(lxr, )


def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	questions = SITE.fetch('questions', fromdate=datetime(2015,1,1), todate=datetime(2018,10,22), min=0, sort='votes', tagged='json', filter='!-*jbN-o8P3E5')
	init_corenlp()
	interesting_sentences = find_interesting_sentences(questions)

	for interesting_sentence in interesting_sentences:
		if isinstance(interesting_sentence, ConditionalSentence):
			interesting_sentence.print('|')
		else:
			interesting_sentence.print("WordPatternBaseline", '|')


if __name__ == "__main__":
	main()
