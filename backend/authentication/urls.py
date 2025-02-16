from django.urls import path
from .views import login_view, google_login, get_user_profile

urlpatterns = [
    path('login/', login_view, name='login'),
    path('google-login/', google_login, name='google_login'),
    path('profile/', get_user_profile, name='profile'),

]
