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

			#we want to consider threads that have at least 2 answers
			if answers is not None and len(answers) >= 2:
				for answer in answers:
					paragraphs = get_paragraphs(answer['body'])
					if paragraphs is not None:
						for paragraph_index, paragraph in enumerate(paragraphs):

							#get conditional sentences (our technique and also includes just sentences with "if")
							cond_sentences = get_cond_sentences(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
							all_interesting_sentences.extend(cond_sentences)

	return all_interesting_sentences

def read_patterns_file():
    patterns = []
    with open("patterns.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            patterns.append([item.strip() for item in items])

    return patterns

def read_question_ids():
    question_ids = list()
    with open("test/question_ids.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            question_ids.extend([item.strip() for item in items])

    return question_ids


def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	questions = read_question_ids();
	init_corenlp()
	interesting_sentences = find_interesting_sentences(questions)

	for interesting_sentence in interesting_sentences:
		if isinstance(interesting_sentence, ConditionalSentence):
			interesting_sentence.print('|')
		else:
			interesting_sentence.print("WordPatternBaseline", '|')


if __name__ == "__main__":
	main()
