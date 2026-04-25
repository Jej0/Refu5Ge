from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllToDos.as_view(), name="index"),
    path("today/", views.TodayToDos.as_view(), name="today"),
    path("test1/", views.Test1.as_view(), name="test1"),
    path("test1/create/", views.add_test, name="test1_create"),
    path("test1/allRooms/", views.AllRooms.as_view(), name="test1_all_rooms"),
    path("rooms/<int:pk>/", views.RoomDetail.as_view(), name="room_detail"), # pour les details d'une room
    path("items/<int:pk>/", views.ItemDetail.as_view(), name="item_detail"),
    path("rooms/<int:pk>/devices/add/", views.room_device_add, name="room_device_add"),
    path("edit/<str:model_name>/<int:object_id>/", views.edit_object, name="edit_object"),
]
