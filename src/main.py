from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags

def find_cond_sentences(questions):
	all_cond_sentences = list()
	for question in questions['items']:
		for answer in question['answers']:
			paragraphs = get_paragraphs(answer['body'])
			for paragraph_index, paragraph in enumerate(paragraphs):
				cond_sentences = get_cond_sentences(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
				all_cond_sentences.extend(cond_sentences)

	return all_cond_sentences

def read_patterns_file():
    patterns = []
    with open("patterns.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            patterns.append([item.strip() for item in items])

    return patterns

def find_word_pattern_sentences(questions, patterns):
	all_word_pattern_sentences = list()
	for question in questions['items']:
		for answer in question['answers']:
			paragraphs = get_paragraphs(answer['body'])
			for paragraph_index, paragraph in enumerate(paragraphs):
				word_pattern_sentences = get_word_pattern_sentences(patterns,paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
				all_word_pattern_sentences.extend(word_pattern_sentences)

	return all_word_pattern_sentences

def main():
	load_tags()
	patterns = read_patterns_file()
	SITE = StackAPI('stackoverflow')
	questions = SITE.fetch('questions', ids=[8091428], filter='!-*jbN-o8P3E5')
	#questions = SITE.fetch('questions', fromdate=datetime(2011,11,11), todate=datetime(2011,11,12), min=10, sort='votes', tagged='java', filter='!-*jbN-o8P3E5')
	init_corenlp()
	cond_sentences = find_cond_sentences(questions)
	baseline_sentences = find_word_pattern_sentences(questions, patterns)
	for cond_sentence in cond_sentences:
		cond_sentence.print('|')

	for baseline_sentence in baseline_sentences:
		baseline_sentence.print("WordPatternBaseline", '|')


if __name__ == "__main__":
	main()
