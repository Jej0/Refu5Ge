from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllToDos.as_view(), name="index"),
    path("today/", views.TodayToDos.as_view(), name="today"),
    path("test1/", views.Test1.as_view(), name="test1"),
    path("test1/create/", views.add_test, name="test1_create"),
    path("edit/<str:model_name>/<int:object_id>/", views.edit_object, name="edit_object"),
]

