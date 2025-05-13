# CS458-Project-Part3

----------------------------------------------------------------------------------
# FOLDER STRUCTURE
----------------------------------------------------------------------------------
- backend/
  - authentication/ 
  - backend/
  - prev_tests/ -- these includes test used in project 1 and 2.
  - tdd_dev/ -- these are the tests used for project 3
  - .env -- you should provide your credentials
  - db.sqlite3
  - manage.py
  - requirements.txt
- frontend/
- venv/
- .gitignore
- README.md



----------------------------------------------------------------------------------
# TO SETUP
----------------------------------------------------------------------------------
# create a venv
- Move to backend 
python -m venv venv
source venv/bin/activate


# install requirements
pip install -r requirements.txt


----------------------------------------------------------------------------------
# HOW TO RUN SPECIFIC PARTS
----------------------------------------------------------------------------------
# Run Backend
-  Move to backend
python manage.py runserver


# Run Frontend
-  Move to frontend
npm install
npm start


# TDD Tests
- Move to backend 
To run all tests: python3 manage.py test tdd_dev 


----------------------------------------------------------------------------------
# MANUEL LOGIN INSTURCTIONS
----------------------------------------------------------------------------------
## Regular Login:
-------------------------
1. Run backend, run frontend.
2. Enter one of the valid user credentials ("username", "password") from `static_data/user.json`. Or make sure you add new mock credentials.
3. Click login.
4. It makes you do dashboard.
5. Choose either going to fill survey page or build survey page.


## Google Login:
-------------------------
1. Go to `static_data/user.json` and add a valid Gmail account that you can log in with. Since there is no registration, it mocks the registration of the email to the system. No need to provide the actual password of your Gmail account, just give a mock password. Do not leave it blank or null.
2. Run the backend and frontend.
3. Click "Google ile Oturum Açın" or in English "Sign in with Google".
4. You will be redirected to the Google login service. Enter your credentials (i.e., your Google account). Remember, the Google account must be valid.
5. same as regular login.


----------------------------------------------------------------------------------
# !!! ATTENTITON !!! ACTIONS TO TAKE BEFORE RUNNING THE TESTS ABOUT GOOGLE LOGIN 
----------------------------------------------------------------------------------
1. In order to test google login, first create a brand new google account. It needs to be Turkish.
2. Add a recovery phone number and login to this account from your phone. It will be needed since Google has some precautions and security rules about logins.
3. Add your account's mail address and actual password to `.env` file. Fields are `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `G_MAIL` `G_PASS` and `G_APP_PASS` respectively. If no such file, create it like /backend/.env
4. During the tests be ready to choose security number from your phone. During login Google asks it. If it say do you want to add passkey, choose no. If test fails, then run once more. This time it wont be asked to add passkey and test will go on.