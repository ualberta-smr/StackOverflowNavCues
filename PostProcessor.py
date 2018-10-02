from stackapi import StackAPI
from datetime import datetime
from bs4 import BeautifulSoup

def get_paragraphs(post_content):
	paragraphs = list()
	soup = BeautifulSoup(post_content, "lxml")

	for paragraph in soup.find_all('p'):
		paragraphs.append(paragraph.get_text())

	return paragraphs


SITE = StackAPI('stackoverflow')
questions = SITE.fetch('questions', fromdate=datetime(2011,11,11), todate=datetime(2011,11,19), min=10, sort='votes', tagged='java', filter='!-*jbN-o8P3E5')
for question in questions['items']:
	for answer in question['answers']:
		paragraphs = get_paragraphs(answer)
		for paragraph in paragraphs:
			text_processor = TextProcessor(paragraph)
			text_processor.annotate_input()
