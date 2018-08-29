# Benyamin-Conditional-Insights-Extraction
This repository holds the code and documents related to the conditional insights extraction part of the thesis. 


## Important note

In order to use the code in this repository, you need to download a Stack Overflow dump and extract the "Posts.xml" file which is very large (~70GB) and place that file in the root folder of this repo. 

## Structure

Baseline.py is a script to identify sentences from Stack Overflow text that match any of the word patterns that are included in patterns.txt. This is the word patterns that were based on Martin's paper of finding "useful sentences" (indispensible knowledge) in documentation. This was supposed to be the baseline we compare to, but actually didn't really work out in the end.

read_db.py is a script that needs a database file called "Witt.db" to work. I did not include the file here since it's too large (~1.4GB) but it's available on Google drive. This script extracts all the Stack Overflow tags (included in Tags.xml) and identifies their classification from the Witt.db database. It returns a dictionaty that other scripts use but can be modified to do anything you want with those classifications. 


regex.py is simply a list of regular expressions used to identify code terms in Stack Overflow text. 

Script.py reads the "Posts.xml" file and identifies conditional insight sentences and writes to standard output. The output is formatted in the form of a Markdown table so that if you copy the output straight to a github .md file you'll see the table. You can obviously modify this part for your purposes. If you want the output in the form of a csv, you can just pipe STDOUT to a .csv file and open it with the "|" character as the delimiter. 


tags.py reads the "Tags.xml" file and also includes a list of the keywords related to non functional requirements (from Abram Hindle's work) and also a list of modal verbs (which is something we looked into before and later gave up on). 
