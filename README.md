## Extracting Navigation Cues from Stack Overflow

When navigating a given Stack Overflow thread, users may want to quickly spot certain sentences in an answer to decide if they want to read it or navigate it past it. We call these sentences *essential sentences*. This repository contains the code we used for extracting essential sentences using four approaches in our SANER 2020 paper "Essential Sentences for Navigating Stack Overflow Answers". If you are looking for the complete artifact page, which includes the survey results etc.,  please check [https://github.com/ualberta-smr/saner2020-artifactpage](https://github.com/ualberta-smr/saner2020-artifactpage).

### Prerequisites

* This code uses `python3`. Make sure you have python > 3.0 installed
* The list of python packages used can be found in `requirements.txt`. You can individually install them or do `pip install -r requirements.txt`

### How to Run

1. Create a StackExchange application key to be able to use the higher query limit at [https://stackapps.com/apps/oauth/register](StackExchange). In `SOAnalysisCode/src/main.py`, update the line `SITE = StackAPI('stackoverflow', key='ADD YOUR KEY HERE')` with your key.

2. Run Stanford CoreNLP server running. This can be done by downloading the Stanford Core NLP [lib files](https://stanfordnlp.github.io/CoreNLP/download.html) first. The one we downloaded was `stanford-corenlp-full-2018-02-27.zip`. After unzipping and changing to the unzipped folder, run:
`java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000` 

3. In a different terminal, run `python3 src/main.py > output`. This will extract sentences by simpleif, wordpatterns, and contextif. Format of output file is described below. Note that the patterns we use for the wordpatterns technique are available in the `patterns.txt` file. Also, note that this will produce a `stats.txt` file that contains statistics about number of paragraphs, sentences etc processed

4. Getting lexrank sentences:

	* Put the ids of your target threads in `lexrank/question_ids.txt`. The current file already contains the IDs of the 20 threads we used in our survey. 
	* To extract processed paragraphs (no html tags, links removed, and lemmatized words in the sentences) to be used with the lexrank approach, run `python3 src/lexrank.py`. This script reads the target question ids from the `question_ids.txt` file and then outputs the paragraph text of each thread from there in the `lexrank` directory. Each thread has a corresponding text file. You can already find the results of running this on the 20 threads in the `lexrank` folder.
	* For each thread, simply concatenate the text in that file, and follow the instructions in the lexrank implementaiton we use at [https://github.com/linanqiu/lexrank](https://github.com/linanqiu/lexrank). Note that the exact `lexrank` call we use for each thread, and the returned selected sentence can also be found in the `lexrank` folder. The files are named `<threadID>-lex.txt`. In case the original lexrank implementation becomes unavailable, we have also created a fork at [https://github.com/ualberta-smr/lexrank](https://github.com/ualberta-smr/lexrank).

**IMPORTANT:** The SO query in our current code is hard-coded to the scope of our evaluation (json threads with score > 0 and asked between March 29, 2018 to March 29, 2019. If you want to run this for different data, make sure to update the query in `src/main.py`. The following line is what you are looking for `questions = SITE.fetch('questions', fromdate=datetime(2018,3,29), todate=datetime(2019,3,29), min=0, sort='votes', tagged='json', filter='!-*jbN-o8P3E5')`

### Interpreting the Output format

The output file will contain a `|`-separated output that matches the following header order 
`IsInsightFulIf|QuestionID|AnswerID|ParagraphIndex|SentenceIndex|Sentence|IsTruePositive|Condition|TagsInCondition|NFReqs|Nouns|Interrogative?|IsFirstPerson?|IsUnsurePhrase?|HasUsefulGrammarDep?`
You can change the delimeter used in `src/main.py`.

Note that the `IsInsightFulIf` column will be `False` if the sentence is a simpleif sentence, will be `True` if the sentence is a contextif sentence, and will be `WordPatternBaseline` if the sentence is a wordpattern sentence. 

For the wordpattern technique, only the first 6 columns make sense. The remaining columns simply show information relevant to conditional sentences to help analyze the output.

Please note that the `IsTruePositive` only makes sense in the context of benchmarking below. Ignore it when running normally.

### Tests

The `src/test.py` file has some unit tests for the individual heuristics to make sure they work correctly.

### Benchmarks 

We have a benchmark of 113 manually labelled sentences that we used to test various heuristics while developing the contextif technique. The data for the benchmark is in the `benchmark` folder. `json_question_ids.txt` contains the Thread/Question ids of the threads involved in the benchmark and `benchmark_json_questions.csv` contains the ground truth.

To run the benchmark, run `python3 src/run_benchmark.py`. The combination of heuristics is documented in this python file. The script calculates and outputs the precision and recall of each heuristic combination against the benchmark.
The sentences detected by each combination of heuristics will be saved in the `benchmark/results` folder.

**IMPORTANT:** Take these numbers with a grain of salt, since the benchmark is not based on looking at *all* sentences in the threads. Instead, we manually analyzed conditional sentences (those with if conditions) and decided if they are useful conditions or not. Thus, there may be other sentences in the thread that are useful but are not conditional sentences. The relative performance of heuristics is what counts here.
