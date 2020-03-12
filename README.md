# Simple Ticketing Platform Built using Django

## Requirements
python2.7
unix
virtualenv
postgresql

## To setup project
* create postgresql database, ensuring db name and credentials match value in `arm/settings.py`
* setup virtual environment
  * `virtualenv venv`
* Enter virtual environment
  * `source venv/bin/activate`
* Install required packages
  * `pip install -r requirements.txt`

### To run app
* `python manage.py runserver`

* Navigate to 
  * `http://localhost:8000` to view app
  * `http://localhost:8000/api/v1` for API endpoints

