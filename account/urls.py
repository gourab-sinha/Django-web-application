from django.urls import path
from django.contrib.auth import views as auth_views
from account import views as account_views

app_name = "account"
urlpatterns = [
    path('register/', account_views.register, name="register"),
    path('manager/', account_views.manager, name="manager"),
    path('user/', account_views.user, name="user"),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name="logout"),
]