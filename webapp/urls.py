from django.urls import path
from . import views
app_name = "app_webapp"
urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("discussion/", views.DiscussionView.as_view(), name="discussion"),
    path("assignments/",views.AssignmentView.as_view(), name="assignment"),
    path("", views.HomeView.as_view(), name="dashboard"),
]
