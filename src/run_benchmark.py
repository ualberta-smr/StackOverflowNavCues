from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags
import csv

#This file runs our analysis against the manually created benchmark to compare the effect of the different heuristics

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
	with open("benchmark/data/json_question_ids.txt", "r") as file: 
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
    list3 = set(list1).intersection(set(list2))#[value for value in list1 if value in list2] 
    return list3

def load_benchmark():
	benchmark = list()
	entries = csv.DictReader(open("benchmark/data/benchmark_json_questions.csv"))
	for entry in entries:
		cond_sentence = ConditionalSentence(sentence=None, question_id = int(entry['QuestionID']), answer_id = int(entry['AnswerID']), paragraph_index=int(entry['ParagraphIndex']), sentence_pos=int(entry['SentenceIndex']), insightful=str_to_bool(entry['Insightful']))
		benchmark.append(cond_sentence)

	return benchmark

#https://stackoverflow.com/questions/3013449/list-comprehension-vs-lambda-filter
#Poster: Duncan
def filter_by_value(list, value):
   for sentence in list:
       if sentence.is_insightful == value: yield el

def calculate_perf_metrics(heuristic, heuristic_sentences, benchmark):
	print("=========== Calculating for " + heuristic)

	predicted_size = len(heuristic_sentences)
	benchmark_size = len(benchmark)
	print("predicted size: " + str(predicted_size))
	recall = 0
	precision = 1

	if predicted_size != 0:
		benchmark_yes = [sentence for sentence in benchmark if sentence.is_insightful() == True]
		benchmark_yes_size = len(benchmark_yes)
		# benchmark_no = [sentence for sentence in benchmark if sentence.is_insightful() == False]
		# benchmark_no_size = len(benchmark_no)

		#calculate recall and precision
		intersection_yes = get_intersection(benchmark_yes, heuristic_sentences)	
		intersection_yes_size = len(intersection_yes)
		recall = intersection_yes_size/benchmark_yes_size
		precision = intersection_yes_size/predicted_size

		print(heuristic + ", intersection size = " + str(intersection_yes_size))

		#set true positives to true... this is extremely inefficient
		for sentence in heuristic_sentences:
			if sentence in intersection_yes:
				sentence.set_true_positive(True)

	print(heuristic +  ", recall=" + str(recall))
	print(heuristic + ", precision=" + str(precision))


def print_output(filename, output):

	file = open(filename, "w")
	fieldnames = ["QuestionId", "AnswerID", "ParagraphIndex", "SentenceIndex", "Sentence", "TruePositive?", "Condition", "Tags In Condition", "NFReqs", "Nouns", "IsFirstPerson?", "IsUnsurePhrase?", "HasWantedGrammerDep?"]
	output_writer = csv.writer(file, delimiter='|')
	output_writer.writerow(fieldnames)
	for sentence in output:
		sentence.print('|', output_writer)

def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	question_ids = read_question_ids();
	benchmark = load_benchmark()

	print ("Benchmark size: " + str(len(benchmark)))
	# print ("Insightful count: " + str(len(benchmark_yes)))
	# print ("Not Insightful count: " + str(len(benchmark_no)))
	all_interesting_sentences = list()
	init_corenlp()

	total_true_positive = 0
	total_false_positive = 0
	total_false_negative = 0

	#there is a limit to the number of questions you can pass so we'll do it in chunks of 20
	#find all interesting sentences and store them, then we will process them
	for start in range(0, len(question_ids), 20):
		end = start + 20
		if (end >= len(question_ids)):
			end = len(question_ids) - 1

		questions = SITE.fetch('questions', ids=question_ids[start:end], filter='!-*jbN-o8P3E5')

		all_interesting_sentences.extend(find_interesting_sentences(questions))

	#Create the sets of sentences for each heuristic combination
	##### Heuristics:
	#########Heuristic 1: If any noun in the conditional phrase is a SO tag, then this is a "useful" sentence
	#########Heuristic 2: Grammatical Relationships
	#############Heuristic 2.1: The "if" must be related to a verb and that verb must have a dependency on a noun
	#############Heuristic 2.2: OR the "if" must be related to a noun
	#########Herustic 3: Conditional sentences that are actually question phrases are not "useful"
	#########Heursitc 4: If there is a first person reference "I" after the "if", this sentence is not "useful"
	#########Heurstic 5: Sentences containing uncertainty with phrases like "I don't know" or "I'm not sure" are not useful

	basic_H1 = list()
	H1_H2_1 = list()
	H1_H2_2 = list()
	H1_H2 = list()
	H1_H2_H3 = list()
	H1_H2_H3_H4  = list()
	H1_H2_H3_H4_H5 = list()


	for interesting_sentence in all_interesting_sentences:
		is_h2_1 = False
		is_h2_2 = False

		if interesting_sentence.has_so_tag():
			basic_H1.append(interesting_sentence)

			if interesting_sentence.has_valid_vb_dep():
				H1_H2_1.append(interesting_sentence)
				is_h2_1 = True

			if interesting_sentence.has_valid_noun_dep():
				H1_H2_2.append(interesting_sentence)
				is_h2_2 = True

			if is_h2_1 or is_h2_2:
				H1_H2.append(interesting_sentence)

				if not interesting_sentence.is_interrogative():
					H1_H2_H3.append(interesting_sentence)

					if not interesting_sentence.is_first_person():
						H1_H2_H3_H4.append(interesting_sentence)

						if not interesting_sentence.is_unsure_phrase():
							H1_H2_H3_H4_H5.append(interesting_sentence)



	print_output("benchmark/results/basic_H1.csv", basic_H1)
	calculate_perf_metrics("basic_H1", basic_H1, benchmark)

	print_output("benchmark/results/H1_H2_1.csv", H1_H2_1)
	calculate_perf_metrics("H1_H2_1", H1_H2_1, benchmark)

	print_output("benchmark/results/H1_H2_2.csv", H1_H2_2)
	calculate_perf_metrics("H1_H2_2", H1_H2_2, benchmark)

	print_output("benchmark/results/H1_H2.csv", H1_H2)
	calculate_perf_metrics("H1_H2", H1_H2, benchmark)

	print_output("benchmark/results/H1_H2_H3.csv", H1_H2_H3)
	calculate_perf_metrics("H1_H2_H3", H1_H2_H3, benchmark)

	print_output("benchmark/results/H1_H2_H3_H4.csv", H1_H2_H3_H4)
	calculate_perf_metrics("H1_H2_H3_H4", H1_H2_H3_H4, benchmark)

	print_output("benchmark/results/H1_H2_H3_H4_H5.csv", H1_H2_H3_H4_H5)
	calculate_perf_metrics("H1_H2_H3_H4_H5", H1_H2_H3_H4_H5, benchmark)



if __name__ == "__main__":
	main()
