# Clinical Trials

In this project, our goal is to rank clinical trials based on provided inclusion/exclusion criteria.

1. Download Cancer-related trials from https://clinicaltrials.gov/, put the files at local path.

2. Change the path for files and index in file_path.txt under searchapp/ ,then index all the trials files with Whoosh:
 cd [searchapp_path]
 python index.py

3. Run the search app which allows user to input patient information with Flask framwork:
 cd [searchapp_path]
 python run.py

4. To launch the server, open http://localhost:5000 on the browser.

5. Input the patient file, gender and age are required, biomarker is optional. Click "Go" to search.

6. The info will be used as creating a patient object for searching query

7. Results will be returned with highlighted matching biomarker terms.

Notice: Anytime the trials files are changed, documents need to be indexed again
The results are returned in a ranking order, use the NCT id to track the trail you are interested.





