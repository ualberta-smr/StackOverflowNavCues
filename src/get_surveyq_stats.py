##Given a set of questions, this script retreives the number of answers for each question
from stackapi import StackAPI
from statistics import median

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
		for question in items:
			answers = question.get('answers')
			print (question['question_id'], len(answers))
			answer_counts.append(len(answers))

		print("Median answer count: ", median(answer_counts))
		print("Min answer count: ", min(answer_counts))
		print("Max answer count: ", max(answer_counts))

if __name__ == "__main__":
	main()