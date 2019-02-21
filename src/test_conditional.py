from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags
import csv

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
							cond_sentences = get_cond_sentences_from_para(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
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
	with open("tests/json_question_ids.txt", "r") as file: 
		for line in file.readlines():
			question_ids.append(int(line.strip()))

	return question_ids


def str_to_bool(string):
	if string.strip().lower() == "true":
		return True

	if string.strip().lower() == "false":
		return False

#https://www.geeksforgeeks.org/python-intersection-two-lists/
def get_intersection(list1, list2):
    list3 = [value for value in list1 if value in list2] 
    return list3

def create_benchmark():
	benchmark = list()
	entries = csv.DictReader(open("tests/benchmark_json_questions.csv"))
	for entry in entries:
		cond_sentence = ConditionalSentence(sentence=None, question_id = entry['QuestionID'], answer_id = entry['AnswerID'], paragraph_index=entry['ParagraphIndex'], sentence_pos=entry['SentenceIndex'], insightful=str_to_bool(entry['Insightful']))
		benchmark.append(cond_sentence)

#https://stackoverflow.com/questions/3013449/list-comprehension-vs-lambda-filter
#Poster: Duncan
def filter_by_value(list, value):
   for sentence in list:
       if sentence.is_insightful == value: yield el

def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	question_ids = read_question_ids();
	benchmark = create_benchmark()

	total_true_positive = 0 
	total_false_positive = 0
	total_false_negative = 0

	#there is a limit to the number of questions you can pass so we'll do it in chunks of 20
	for start in range(0, len(question_ids), 20):
		end = start + 20
		if (end >= len(question_ids)):
			end = len(question_ids) - 1

		questions = SITE.fetch('questions', ids=question_ids[start:end], filter='!-*jbN-o8P3E5')
		init_corenlp()
		interesting_sentences = find_interesting_sentences(questions)
		[sentence.print('|') for sentence in interesting_sentences]
		
		intersection = get_intersection(benchmark, interesting_sentences)
		total_true_positive += filter_by_value(intersection, True)
		total_true_negative ??? 


if __name__ == "__main__":
	main()
