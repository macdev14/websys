from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("delete", views.delete_account, name="delete"),
    path("profile", views.UserUpdateView.as_view(), name="mydata"),
    path("profile/credencial", views.UpdatePassword.as_view(), name="passupdate"),
    
]