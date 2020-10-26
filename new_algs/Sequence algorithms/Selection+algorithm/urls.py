from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r"^login/$", auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    url(r"^signup/$", views.SignUp.as_view(), name="signup"),
]