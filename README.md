# CS458-Project-Part1

# creating venv
- Move to backend 
python -m venv venv
source venv/bin/activate


# install requirements
pip3 install requirements.txt


# Run Backend
-  Move to backend
python manage.py runserver


# Run Frontend
-  Move to frontend
npm install
npm start


# Test
- Move to backend/authentication/test 
pytest tests.py -s


To run the application first run backend and then run frontend. And then tests are ready to run.

## kendimize notlar !! silinecek 
# NE NEREDE ?? 
views.py -> login fonskiyonlarının oldugu yer
login.js -> login frontend
tests/tests.py -> testlerimiz
tests/selenium_capabilities.py -> selenium işleri
static_data/users.json -> datamız
