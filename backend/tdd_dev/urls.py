from django.urls import path
from .views import login_view, google_login, submit_survey

urlpatterns = [
    path('login/', login_view, name='login'),
    path('google-login/', google_login, name='google_login'),
    path('submit-survey/', submit_survey, name='submit_survey'),
]