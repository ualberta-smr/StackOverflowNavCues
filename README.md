# Extracting conditional insight sentences

This repository holds the code and documents related to extracting conditional insight sentences. 


## Important note

In order to use the code in this repository, you need to download a Stack Overflow dump and extract the `Posts.xml` file which is very large (~70GB) and place that file in the root folder of this repo. 

## Structure

* `baselines` is a folder containing the different baselines we can compare to for our work. [`WordPatternBaseline.py`](https://github.com/ualberta-smr/Benyamin-Conditional-Insights-Extraction/blob/master/baseline.py) is a script to identify sentences from Stack Overflow text that match any of the word patterns that are included in [`patterns.txt`](https://github.com/ualberta-smr/Benyamin-Conditional-Insights-Extraction/blob/master/patterns.txt). These are the word patterns that are based on Martin Robillard's paper of finding "useful sentences" (indispensible knowledge) in documentation. Simply using the patterns from the word list did not work well. To try to generalize from there, the current script ignores order in the patterns and the CW term. However, that still did not improve the results much.

read_db.py is a script that needs a database file called "Witt.db" to work. I did not include the file here since it's too large (~1.4GB) but it's available on Google drive. This script extracts all the Stack Overflow tags (included in Tags.xml) and identifies their classification from the Witt.db database. It returns a dictionaty that other scripts use but can be modified to do anything you want with those classifications. This was Christoph's Witt database that we wanted to use to identify the type of tag (e.g., language, OS etc.), but we didn't end up using it and just simplified things to say we are interested in all sentences that have a conditional phrase matching a tag.


regex.py is simply a list of regular expressions used to identify code terms in Stack Overflow text. 

Script.py reads the "Posts.xml" file and identifies conditional insight sentences and writes to standard output. The output is formatted in the form of a Markdown table so that if you copy the output straight to a github .md file you'll see the table. You can obviously modify this part for your purposes. If you want the output in the form of a csv, you can just pipe STDOUT to a .csv file and open it with the "|" character as the delimiter. 


tags.py reads the "Tags.xml" file and also includes a list of the keywords related to non functional requirements (from Abram Hindle's work) and also a list of modal verbs (which is something we looked into before and later gave up on). 
