from datetime import date

from django.shortcuts import redirect, render, get_object_or_404
from django.apps import apps

# Create your views here.
from django.views.generic import ListView, UpdateView, DetailView
from .models import *
from .forms import *

def home(request):
    return render(request, 'core/home.html')


class AllRooms(ListView):
    model = Room
    template_name = "core/allRooms.html"

    def get_queryset(self):
        return Room.objects.all()

class RoomDetail(DetailView):
    model = Room
    template_name = "core/room_detail.html"
    context_object_name = "room"

class ItemDetail(DetailView):
    model = Device
    template_name = "core/item_detail.html"
    context_object_name = "item"


def edit_object(request, model_name, object_id):
    """Vue générique pour éditer n'importe quel modèle"""
    try:
        model = apps.get_model('core', model_name)
    except LookupError:
        return render(request, "core/error.html", {"error": f"Modèle '{model_name}' non trouvé"})

    obj = get_object_or_404(model, pk=object_id)
    form_class = get_generic_form(model)

    if request.method == "POST":
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("home")  # Redirection après édition
    else:
        form = form_class(instance=obj)

    return render(request, "core/edit.html", {
        "form": form,
        "object": obj,
        "model_name": model_name,
    })
