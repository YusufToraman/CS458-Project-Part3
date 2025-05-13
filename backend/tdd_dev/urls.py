from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view, google_login, submit_survey, survey_build

urlpatterns = [
    path('login/', login_view, name='login'),
    path('google-login/', google_login, name='google_login'),
    path('submit-survey/', submit_survey, name='submit_survey'),
    path('survey-build/', survey_build, name='survey_build'),
]
