import re
import csv
import pdb
from bs4 import BeautifulSoup
import xml.etree.ElementTree as etree
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP

core_obj = None

def get_core_obj():
    global core_obj
    if not core_obj:
        core_obj = pycorenlp_StanfordCoreNLP('http://localhost:9000')

    return core_obj

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
    questions = SITE.fetch('questions', fromdate=datetime(2011,11,11), todate=datetime(2011,11,12), min=10, sort='votes', tagged='java', filter='!-*jbN-o8P3E5')
    init_corenlp()
    cond_sentences = find_cond_sentences(questions)
    for cond_sentence in cond_sentences:
        cond_sentence.print('|')


if __name__=="__main__":
    patterns = read_patterns_file()
    for event, elem in etree.iterparse('Posts.xml', events=('start', 'end')):
        if event == "start":
            if elem.tag == "row":
                if elem.attrib["PostTypeId"] == "2": # and elem.attrib["ParentId"] == THREAD_ID: 

                    XML_parsed = parse_xml_line(elem, patterns)
                    print("checked one element")

                    for item in XML_parsed:
                        print(item)

                    if XML_parsed: pdb.set_trace()