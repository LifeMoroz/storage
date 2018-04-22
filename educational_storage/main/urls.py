from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url (r'^home/', views.home, name="home"),
    url (r'^login/', views.login, name="login"),
    url (r'^registration/', views.registration, name="registration"),
    url (r'^favorites/', views.favorites, name="favorites"),
    url (r'^search/', views.search, name="search"),
    url (r'^storage/', views.storage, name="storage"),
    url (r'^files/', views.files, name="files"),
    url (r'^load/', views.load, name="load"),
]
