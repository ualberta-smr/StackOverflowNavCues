from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import sys

def get_paragraphs(post_content):
	paragraphs = list()
	
	only_p_tags = SoupStrainer("p")
	soup = BeautifulSoup(post_content, "lxml", parse_only=only_p_tags)


	for paragraph in soup:
		#replace all link text with LINK
		for a in paragraph.findAll('a'):
  			a.string = "LINK"


		#replace all code tags with CW
		#for a in paragraph.findAll('code'):
  		#	a.string = "CW"

		paragraphs.append(paragraph.get_text())

	#print("===========", file=sys.stderr)
	#print(paragraphs, file=sys.stderr)
	return paragraphs
