If it's the first time to launch the app, please modify the all the file paths in file_path.txt first, then run the index.py to index the documents.
Anytime the trials files are changed, documents need to be indexed again

Here is the Flask application to search over the trials.
Run ./run.py to launch the server, then open up http://localhost:5000

Please fill out all the informations(select the age) on the page regarding the patient file, then click "Go".
Results match the patient file will be shown and the match terms for biomarker are highlighted.
The results are returned in a ranking order, use the NCT id to track the trail you are interested.




