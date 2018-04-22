from django.urls import path, re_path

from app.main import legacy_views
from . import views


app_name = 'main'

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('login/', views.SignIn.as_view(), name="signin"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('logout/', views.SignOut.as_view(), name="signout"),
    re_path('search/', views.Search.as_view(), name='search'),
    re_path('storage/(?P<pk>\d+)', views.Storage.as_view(), name="storage"),
    re_path('course/(?P<pk>\d+)', views.CourseDetail.as_view(), name="course"),
    # path('files/', views.files, name="files"),
    # path('load/', views.load, name="load"),

    re_path('favorites/remove/(?P<fid>\d+)/', views.FavoritesRemove.as_view(), name='favorites-remove'),
]
