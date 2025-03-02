# CS458-Project-Part1

----------------------------------------------------------------------------------
# TO SETUP
----------------------------------------------------------------------------------
# creating venv
- Move to backend 
python -m venv venv
source venv/bin/activate


# install requirements
pip3 install requirements.txt


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


# Test
- Move to backend/authentication/test 
To run all tests: pytest tests.py -s 
To run a specific test: pytest tests.py -k "< test_function_name >"


----------------------------------------------------------------------------------
# MANUEL LOGIN INSTURCTIONS
----------------------------------------------------------------------------------

## Regular Login:
-------------------------
1. Run backend, run frontend.
2. Enter one of the valid user credentials ("username", "password") from `static_data/user.json`. Or make sure you add new 
credentials.
3. Click login.
4. You will be directed to the mock dashboard page.
5. You can logout by clicking the logout button.


## Google Login:
-------------------------
1. Go to `static_data/user.json` and add a valid Gmail account that you can log in with. Since there is no registration, it mocks the registration of the email to the system. No need to provide the actual password of your Gmail account, just give a mock password. Do not leave it blank or null.
2. Run the backend and frontend.
3. Click "Google ile Oturum Açın" or in English "Sign in with Google".
4. You will be redirected to the Google login service. Enter your credentials (i.e., your Google account). Remember, the Google account must be valid.
5. You will be directed to the mock dashboard page.
6. You can log out by clicking the logout button.


To run the application, first run the backend and then run the frontend. After that, the tests are ready to run.
