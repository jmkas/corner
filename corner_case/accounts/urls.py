from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = "accounts"
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name="reg_view"),
    path('login/', obtain_auth_token, name="login_view")
]

urlpatterns = format_suffix_patterns(urlpatterns)
