from bs4 import BeautifulSoup

def get_paragraphs(post_content):
    paragraphs = list()
    soup = BeautifulSoup(post_content, "lxml")

    for paragraph in soup.find_all('p'):
        paragraphs.append(paragraph.get_text())

    return paragraphs

def get_all_posts_from_xml(filename):
	for event, elem in etree.iterparse(filename, events=('start', 'end')):
        # if counter < 100:
        #     counter += 1
        #     continue

        # if counter  >= 563:
        #     exit()

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