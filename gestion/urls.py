from django.urls import path
from . import views

urlpatterns = [
    path("allRooms/", views.AllRooms.as_view(), name="all_rooms"),
    path("rooms/<int:pk>/", views.RoomDetail.as_view(), name="room_detail"),  # pour les details d'une room
    path("items/<int:pk>/", views.ItemDetail.as_view(), name="item_detail"),
    path("rooms/<int:pk>/devices/add/", views.room_device_add, name="room_device_add"),
    path("edit/<str:model_name>/<int:object_id>/", views.edit_object, name="edit_object"),
    path("device/<int:pk>/toggle/", views.toggle_device, name="toggle_device"),

]
