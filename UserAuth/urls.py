from django.urls import path
from .views import RegisterUser,LoginUser,LogoutUser,changePassword

urlpatterns = [
    path("register/",RegisterUser,name='Register'),
    path("login/",LoginUser,name='login'),
    path("logout/",LogoutUser,name='logout'),
    path("changepassword/",changePassword,name='changepassword'),
]