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


def parse_xml_line(el, patterns):
    result = []
    soup = BeautifulSoup(el.attrib["Body"], "lxml")
    all_text = ""
    for item in soup.find_all('p'):
        all_text += item.get_text()

    corenlp = get_core_obj()
            
    annotated = corenlp.annotate(all_text, properties = {
        'annotators': 'pos,parse',
        'outputFormat': 'json'
    })

    for sentence in annotated['sentences']:
        if check_sentence(sentence, patterns):
            result.append(sentence)
        
    return result

def get_sentence(annotated):
    res = ""
    for word in annotated['tokens']:
        res += word['word'] + " "
    return res


def check_sentence(sentence, patterns):
    sentence_text = get_sentence(sentence)
    found_match = False

    for pattern in patterns:
        all_found = True
        for item in pattern:
            if item == "CW":
                continue
            if not item in sentence:
                all_found = False
                break

        if all_found:
            return True





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