from bs4 import BeautifulSoup

def get_paragraphs(post_content):
    paragraphs = list()
    soup = BeautifulSoup(post_content, "lxml")

    for paragraph in soup.find_all('p'):
        paragraphs.append(paragraph.get_text())

    return paragraphs