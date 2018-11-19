# Extracting conditional insight sentences

This repository holds the code and documents related to extracting conditional insight sentences. 

# Prereqisites 

* This code uses `python3`. Make sure you have python > 3.0 installed
* The list of python packages used can be found in `requirements.txt`. You can individually install them or do `pip install -r requirements.txt`


# How to Run

1. Make sure you have the Stanford CoreNLP server running. This can be done by downloading the Stanford Core NLP [lib files](https://stanfordnlp.github.io/CoreNLP/download.html) first. After unzipping, you can run:

`java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000`

2. Run `python3 src/main.py > output`. 

3. To extract processed paragraphs (no html tags, links removed, and lemmatized words in the sentences) to be used with the lexrank approach, run `python3 src/lexrank.py`. This script reads question ids from the `question_ids.txt` file and then outputs the paragraph text of each thread from there in a `lexrank` directory.

# Output format

The output file will contain a `|`-separated output that matches the following header order `IsConditional|Question ID| Answer ID|Paragraph index|Sentence Position|Sentence| Condition|Tags|NFReqs|Nouns`. You can change the delimter used in `main.py`. Also, note that we currently print all sentences having `if` and mark the ones that match our criteria (i.e., have nouns matching SO tags in their condition) as True in the first column. This allows us to use all those that are False (i.e., just have the word `if` in them) as a naive baseline. 

Right now, there is also output from the baseline technique that relies on matching any of the patterns in match any of the word patterns that are included in [`patterns.txt`](https://github.com/ualberta-smr/Benyamin-Conditional-Insights-Extraction/blob/master/patterns.txt) -- Martin Robillard's indispensible knowledge paper. The output will look the same as above, except that the first column will have the value `WordPatternBaseline` and the last 4 columns specific to conditional sentences will have empty values.


## Structure

* The `unusedfiles` folder under `src` contains old scripts that are currently not used. Just keeping them there now till we figure if we will need them again. The `read_db.py` is a script that needs a database file called "Witt.db" to work. I did not include the file here since it's too large (~1.4GB) but it's available on Google drive. This script extracts all the Stack Overflow tags (included in Tags.xml) and identifies their classification from the Witt.db database. It returns a dictionaty that other scripts use but can be modified to do anything you want with those classifications. This was Christoph's Witt database that we wanted to use to identify the type of tag (e.g., language, OS etc.), but we didn't end up using it and just simplified things to say we are interested in all sentences that have a conditional phrase matching a tag.


* The `src` folder:
    * `regex.py` is simply a list of regular expressions used to identify code terms in Stack Overflow text. 
    * `main.py` is the main entry point of the program. It queries SO through the stackexchange API and then finds all conditional sentences in the paragraphs of the resulting answers. To try out a different technique (e.g. baselines to compare to), you can simply change the call of `find_cond_sentences` to a call that represents the entry point of the other technique.  
    * `tags.py` reads the "Tags.xml" file and also includes a list of the keywords related to non functional requirements (from Abram Hindle's work) and also a list of modal verbs (which is something we looked into before and later gave up on). 
    * TBD: add other descriptions

## Notes

*  The current baseline pattern-based approach ignores the order of the patterns

