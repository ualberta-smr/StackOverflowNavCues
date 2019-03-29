from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags


def find_interesting_sentences(questions):
	patterns = read_patterns_file()
	all_interesting_sentences = list()

	file = open("stats.txt", "w")


	items = questions.get('items')

	file.write("Num. Threads processed: " + str(len(items)) + "\n")

	answer_count = 0
	sentence_count = 0
	considered_threads = 0
	total_processed_sentences = 0
	total_failed_sentences = 0
	total_paragraphs = 0
	total_failed_paragraphs = 0
	total_conditional_insight = 0
	total_if_sentences = 0
	total_insightful_if_sentences = 0
	word_pattern_count = 0

	if items is not None:
		for question in items:
			answers = question.get('answers')

			all_answer_sentences = list()

			#we want to consider threads that have at least 2 answers
			if answers is not None and len(answers) >= 2:

				considered_threads += 1

				for answer in answers:
					answer_count += 1
					paragraphs = get_paragraphs(answer['body'])
					if paragraphs is not None:
						for paragraph_index, paragraph in enumerate(paragraphs):

							#get conditional sentences (our technique and also includes just sentences with "if")
							cond_sentences, processed_sentences, failed_sentences = get_cond_sentences_from_para(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)

							if cond_sentences is not None:
								all_interesting_sentences.extend(cond_sentences)
								total_conditional_insight
								total_paragraphs += 1
								total_processed_sentences += processed_sentences
								total_failed_sentences += failed_sentences
								total_if_sentences += len(cond_sentences)
								total_conditional_insight += sum(1 for sentence in cond_sentences if sentence.is_insightful())
							else:
								total_failed_paragraphs += 1


							#get baseline 1 sentences based on Martin's patterns
							word_pattern_sentences = get_word_pattern_sentences(patterns,paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
							word_pattern_count += len(word_pattern_sentences)
							all_interesting_sentences.extend(word_pattern_sentences)


	file.write("Total considered threads: " + str(considered_threads) + "\n")
	file.write("Total processed answers (based on considered threads): " + str(answer_count)  + "\n")
	file.write("Avg. num of answers in considered threads: " + str(answer_count/considered_threads) + "\n")
	file.write("Total processed paragraphs: " + str(total_paragraphs) + "\n")
	file.write("Total failed paragraphs: " + str(total_failed_paragraphs) + "\n")
	file.write("Total processed sentences: " + str(total_processed_sentences) + "\n")
	file.write("Total failed sentences: " + str(total_failed_sentences) + "\n")
	file.write("Total if sentences: " + str(total_if_sentences) + "\n")
	file.write("Total insightful if sentences: " + str(total_conditional_insight) + "\n")
	file.write("Total wordpattern sentences: " + str(word_pattern_count) + "\n")
	file.close()
	return all_interesting_sentences

def read_patterns_file():
    patterns = []
    with open("patterns.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            patterns.append([item.strip() for item in items])

    return patterns


def main():
	load_tags()
	SITE = StackAPI('stackoverflow')
	#Get questions from last 3 years: Ran on March 29, 2019
	questions = SITE.fetch('questions', fromdate=datetime(2016,3,29), todate=datetime(2019,3,29), min=0, sort='votes', tagged='json', filter='!-*jbN-o8P3E5')
	init_corenlp()
	interesting_sentences = find_interesting_sentences(questions)

	for interesting_sentence in interesting_sentences:
		if isinstance(interesting_sentence, ConditionalSentence):
			interesting_sentence.print('|')
		else:
			interesting_sentence.print("WordPatternBaseline", '|')


if __name__ == "__main__":
	main()
