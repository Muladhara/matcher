
***GLIMPSE MATCHER***

Glimpse Matcher has the task of identifying, matching and merging records 
  that correspond to the same entities from several databases.
  
The entities under consideration refer to enterprises and people.   

Many name for the same task:
- Entity Resolution 
- Record Linkage 
- Duplicate Detection

Glimpse matcher includes the major steps in data matching process: 
- data pre-processing
- indexing
- record pair comparison
- classification
- clerical review and quality evaluation

----

**Library**

- python 2.7
- py27-levenshtein
- py27-mysql
- py27-django

**How to use**

1. start Glimpse Configurator (python manage.py runserver)
2. go to http://localhost:8000/admin (user/pwd: ele/ele)
3. startup your MySQL
4. define MySQL data sources (input/output), corresponding to the datasets
5. define a cleaning or a matching on the data sources 
6. run the cleaning or the matching from the command line

- run a cleaning
python -m glimpse.main.Main -clean <cleaning_name>

- run a matching
python -m glimpse.main.Main -match <maching_name>
