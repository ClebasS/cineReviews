from django.urls import path
from . import views

app_name = 'sessao'
urlpatterns = [
 path("", views.loginview,
      name="loginview"),
 path("registar", views.registar,
      name="registar"),
 path("criarmoderador", views.criarmoderador,
      name="criarmoderador"),
 path("logout", views.logoutview,
      name='logoutview'),
 path("informacao", views.informacao,
      name='informacao'),
 path('fazer_uploaduser', views.fazer_uploaduser,
      name="fazer_uploaduser"),
]