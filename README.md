# CS458-Project-Part3


----------------------------------------------------------------------------------
# IMPORTANT FILE / FOLDER LOCATIONS
----------------------------------------------------------------------------------
backend/authentication/views.py -> login functionalities
backend/authentication/test/tests.py -> testlerimiz
backend/authentication/tests/selenium_capabilities.py -> selenium helpers
backend/authentication/static_data/users.json -> static data
backend/.env -> environment variables (important for google login)

frontend/src/components/login.js -> login frontend


----------------------------------------------------------------------------------
# TO SETUP
----------------------------------------------------------------------------------
# creating venv
- Move to backend 
python -m venv venv
source venv/bin/activate


# install requirements
pip install requirements.txt


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
mock credentials.
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


----------------------------------------------------------------------------------
# !!! ATTENTITON !!! ACTIONS TO TAKE BEFORE RUNNING THE SELENIUM TESTS ABOUT GOOGLE LOGIN 
----------------------------------------------------------------------------------
1. In order to test google login, first create a brand new google account. It needs to be Turkish.
2. Add a recovery phone number and login to this account from your phone. It will be needed since Google has some precautions and security rules about logins.
3. Add your account's mail address and actual password to `.env` file. Fields are `G_MAIL` and `G_PASS`, respectively. If no such file, create it like /backend/.env
4. During the tests be ready to choose security number from your phone. During login Google asks it. If it say do you want to add passkey, choose no. If test fails, then run once more. This time it wont be asked to add passkey and test will go on.
