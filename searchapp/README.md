If it's the first time to launch the app, please run the index.py to index the documents.
Anytime the trials files are changed, documents need to be indexed again

Here is the Flask application to search over the trials.
Run ./run.py to launch the server, then open up http://localhost:5000/search

Please fill out all the informations(select the age) on the page, then click "Go".
Results match the patient file will be shown and the match terms for biomarker are highlighted.
The results are returned in a ranking order, use the NCT id to track the trail you are interested.

If you want to change the file path for documents or index, go to file_path.txt


