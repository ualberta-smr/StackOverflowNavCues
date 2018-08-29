import re
import csv
import pdb
import time 
import random
import nltk.data
from pyquery import PyQuery
from bs4 import BeautifulSoup
import xml.etree.ElementTree as etree
from stanfordcorenlp import StanfordCoreNLP
from pycorenlp import StanfordCoreNLP as pycorenlp_StanfordCoreNLP
from regex import REGEX_LIST
from tags import load_tags, TAGS_LIST, QUALITY_WORDS, NOUN_IDENTIFIERS
from read_db import get_all_tags

# from taskidentification.taskid import SentenceParser
# from utils.nlputils import VERB_IDENTIFIERS, NOUN_IDENTIFIERS, ADJ_IDENTIFIERS, PATTERNS_LIST

THREAD_ID = "503093"

core_obj = None
all_tags = None

def get_core_obj():
    global core_obj
    if not core_obj:
        core_obj = pycorenlp_StanfordCoreNLP('http://localhost:9000')

    return core_obj

def get_sentence(annotated):
    res = ""
    for word in annotated['tokens']:
        res += word['word'] + " "
    return res

def get_sentences(annotated):
    par = []

    for sentence in annotated['sentences']:
        res = ""
        for word in sentence['tokens']:
            res += word['word'] + " "

        par.append(res)

    return par


def get_ind(snippet):
    count = 0
    for item in snippet:
        if item == " ":
            count += 1
        else:
            return count


def get_tree(items):
    ind = None
    res = []
    for item in items:
        if "in if" in item.lower():
            ind = get_ind(item)
        else:
            if ind:
                if "(, ,)" in item: 
                    return res

                if get_ind(item) >= ind:
                    res.append(get_word(item))

                elif get_ind(item) < ind:
                    return res
            else:
                continue

    return res


def get_word(item):
    res = ""
    for char in item[::-1]:
        if char == " ":
            return res
        elif char == ")":
            continue
        elif char == "(":
            return None
        else:
            res = char + res

    return res



def get_condition(text):
    parsed = text['parse']
    split = parsed.split("\n")
    condition = get_tree(split)

    final = ""
    for item in condition:
        if item:
            final += item + " "

    return final


def get_tags(string):
    res = []
    for word in string:
        if word.lower() in all_tags:
            res.append((word.lower(), all_tags[word.lower()]))
        elif word.lower() in TAGS_LIST:
            res.append(word.lower())

    return res


def get_quartile_tags(string):
    res = []
    for word in re.sub("[^\w]", " ",  string).split():
        if word.lower() in TAGS_LIST and int(TAGS_LIST[word.lower()]) >= 12:
            res.append(word)

    return res


def get_non_func(string):
    res = []
    for word in re.sub("[^\w]", " ",  string).split():
        if word.lower() in QUALITY_WORDS:
            res.append(word)

    return res


def get_nouns(sentence, condition):
    res = []
    words = set(re.sub("[^\w]", " ",  condition).split())
    
    for token in sentence["tokens"]:
        if token["originalText"].lower() in words and token["pos"] in NOUN_IDENTIFIERS:
            res.append(token["originalText"])

    return res

def get_regex_nouns(sentence):
    result = []
    for pattern in REGEX_LIST:
        for word in sentence.split():
            if re.match(pattern, word):
                result.append(word)

    return result


def parse_answer_body(postId, body):
    body = "Why specifically do you need to know if the file is locked anyway ?"
    result = []
    soup = BeautifulSoup(body, "lxml")
    all_text = ""
    for item in soup.find_all('p'):
        all_text += item.get_text()

    corenlp = get_core_obj()
            
    annotated = corenlp.annotate(all_text, properties = {
        'annotators': 'pos,parse',
        'outputFormat': 'json'
    })

    for sentence in annotated['sentences']:
        sentence_text = get_sentence(sentence)
        if " if" in sentence_text.lower():
            condition = get_condition(sentence)
            non_func = get_non_func(condition)
            nouns = list(set(get_nouns(sentence, condition) + get_regex_nouns(sentence_text)))
            tags = get_tags(nouns)


            # exists = True
            # for item in tags:
            #     if not item in el.attrib['Tags']:
            #         exists = False
            # if not exists:
            #     print("YES")

            res = " | " + postId + " | " + sentence_text.replace(",", "") + " | " + condition + " | " + tags.__str__().replace(",","-")     + " | " + non_func.__str__().replace(",","-") + " | " + nouns.__str__().replace(",","-") + " | "

            result.append(res)
        else:
            pass
            # print(sentence_text)
            # pdb.set_trace()

    return result


def parse_xml_line(el):
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
        sentence_text = get_sentence(sentence)
        if " if" in sentence_text.lower():
            condition = get_condition(sentence)
            non_func = get_non_func(condition)
            nouns = list(set(get_nouns(sentence, condition) + get_regex_nouns(sentence_text)))
            tags = get_tags(nouns)

            if not tags:
                # print("NO TAGS")
                return None

            # exists = True
            # for item in tags:
            #     if not item in el.attrib['Tags']:
            #         exists = False
            # if not exists:
            #     print("YES")

            res = " | " + el.attrib["Id"] + " | " + sentence_text.replace(",", "") + " | " + condition + " | " + tags.__str__().replace(",","-")     + " | " + non_func.__str__().replace(",","-") + " | " + nouns.__str__().replace(",","-") + " | "

            result.append(res)
        else:
            pass
            # print(sentence_text)
            # pdb.set_trace()

    return result


def main():
    corenlp = get_core_obj()
    start_time = time.time()
    threads = {}
    tasks_set = set()
    tasks = {}
    counter = 0


    # with open('{}.csv'.format(THREAD_ID), 'r') as csvfile: 
    #     spamreader = csv.reader(csvfile, delimiter=',')
    #     for row in spamreader:
    #         XML_parsed = parse_answer_body(row[0], row[8])

    #         for item in XML_parsed:
    #             print("| {}{}".format(row[3], item).replace("-LRB-", "(").replace("-RRB-", ")").replace(" 't", "'t").replace(" 'd", "'d").replace(" | ", " , ")[1:])

    # exit()

    for event, elem in etree.iterparse('Posts.xml', events=('start', 'end')):
        if counter < 100:
            counter += 1
            continue

        if counter  >= 563:
            exit()

        if event == "start":
            if elem.tag == "row":
                if elem.attrib["PostTypeId"] == "2": # and elem.attrib["ParentId"] == THREAD_ID:
                    if not " if" in elem.attrib["Body"]:
                        continue 

                    XML_parsed = parse_xml_line(elem)
                    
                    if XML_parsed:
                        for item in XML_parsed:
                            print("| {}{}".format(elem.attrib["ParentId"], item).replace("-LRB-", "(").replace("-RRB-", ")").replace(" 't", "'t").replace(" 'd", "'d").replace(" | ", " , ")[1:])
                            
                            # pdb.set_trace()

                        if elem.attrib["ParentId"] in threads: 
                            threads[elem.attrib["ParentId"]] += XML_parsed

                        else:
                            threads[elem.attrib["ParentId"]] = XML_parsed
                            tasks_set.add(elem.attrib["ParentId"])

                        counter += 1
                        # print("COUNTER: {}".format(counter))

                # else:
                #     print(elem.attrib['PostTypeId'])
                #     print(elem.attrib['Id'])
                #     exit()

   
    # for thread, item in threads.items():
    #     pdb.set_trace()
    #     print(thread)
    #     print(item)
    #     print("-"*80)

    # print("--- {} seconds ---".format((time.time() - start_time)))

    # for thread_id, parsed in threads.items():
    #     for item in parsed:
    #         print("| {}{}".format(thread_id, item).replace("-LRB-", "(").replace("-RRB-", ")"))


if __name__=="__main__":
    all_tags = get_all_tags()
    main()