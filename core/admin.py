from django.contrib import admin
from .models import Room, Device, DeviceAttribute, CategorieObjet, ObjetConnecte, Animal, Actualite

admin.site.register(Room)
admin.site.register(Device)
admin.site.register(DeviceAttribute)
admin.site.register(CategorieObjet)
admin.site.register(ObjetConnecte)
admin.site.register(Animal)
admin.site.register(Actualite)
