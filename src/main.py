from stackapi import StackAPI
from datetime import datetime
from so_helper import get_paragraphs
from corenlp_helper import *
from ConditionalSentence import ConditionalSentence
from tags import load_tags


def find_interesting_sentences(questions):
	patterns = read_patterns_file()
	all_interesting_sentences = list()
	for question in questions['items']:
		for answer in question['answers']:
			paragraphs = get_paragraphs(answer['body'])
			for paragraph_index, paragraph in enumerate(paragraphs):

				#get conditional sentences (our technique and also includes just sentences with "if")
				cond_sentences = get_cond_sentences(paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
				all_interesting_sentences.extend(cond_sentences)

				#get baseline 1 sentences based on Martin's patterns
				word_pattern_sentences = get_word_pattern_sentences(patterns,paragraph, q_id=question['question_id'], answ_id=answer['answer_id'], parag_index=paragraph_index)
				all_interesting_sentences.extend(word_pattern_sentences)

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
	questions = SITE.fetch('questions', fromdate=datetime(2011,11,11), todate=datetime(2011,11,12), min=10, sort='votes', tagged='json', filter='!-*jbN-o8P3E5')
	init_corenlp()
	interesting_sentences = find_interesting_sentences(questions)

	for interesting_sentence in interesting_sentences:
		if isinstance(interesting_sentence, ConditionalSentence):
			interesting_sentence.print('|')
		else:
			interesting_sentence.print("WordPatternBaseline", '|')


if __name__ == "__main__":
	main()
