from django.urls import path

from .views import signin, log_out, signup, Google_login, index

urlpatterns = [
    path('', index),
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),
    path('google-login/', Google_login),

]
