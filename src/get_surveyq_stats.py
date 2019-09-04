##Given a set of questions, this script retreives the number of answers for each question
from stackapi import StackAPI
from statistics import median, mean

def read_question_ids():
    question_ids = list()
    with open("lexrank/question_ids.txt", "r") as file: 
        for line in file.readlines():
            items = line.split(",")
            question_ids.extend([item.strip() for item in items])

    return question_ids


def main():
	SITE = StackAPI('stackoverflow')
	question_ids = read_question_ids()
	#get all threads for the ids we are interested in
	questions = SITE.fetch('/questions', ids=question_ids, filter='!-*jbN-o8P3E5')
	
	items = questions.get('items')

	if items is not None:
		answer_counts = []
		sentence_counts = []
		for question in items:
			answers = question.get('answers')
			print (question['question_id'], len(answers))
			answer_counts.append(len(answers))

			for answer in answers:
				paragraphs = get_paragraphs(answer['body'])
				num_of_sentences_in_answer = 0
				if paragraphs is not None:
					for paragraph in paragraphs:
						num_of_sentences_in_answer += len(get_all_paragraph_sentences(paragraph))

				sentence_counts.append(num_of_sentences_in_answer)
							

		print("Median answer count: ", median(answer_counts))
		print("Min answer count: ", min(answer_counts))
		print("Max answer count: ", max(answer_counts))
		print("Total number of sentences in selection:" + sum(sentence_counts))
		print("Median number of sentences per answer: "+ median(sentence_counts))
		print("Mean number of sentences per answer: "+ mean(sentence_counts))
		print("Max number of sentences per answer: " + max(sentence_counts))
		print("Min number of sentences per answer: " + min(sentence_counts))

if __name__ == "__main__":
	main()