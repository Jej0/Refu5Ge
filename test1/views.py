from datetime import date

from django.shortcuts import redirect, render, get_object_or_404
from django.apps import apps
from django.utils.http import url_has_allowed_host_and_scheme

# Create your views here.
from django.views.generic import ListView, UpdateView, DetailView
from .models import *
from .forms import *


class AllToDos(ListView):
    model = ToDoItem
    template_name = "test1/index.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(due_date__gte=date.today())


class TodayToDos(ListView):
    model = ToDoItem
    template_name = "test1/today.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(due_date=date.today())


class Test1(ListView):
    model = Test
    template_name = "test1/test1.html"

    def get_queryset(self):
        return Test.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TestForm()
        return context


class AllRooms(ListView):
    model = Room
    template_name = "test1/allRooms.html"

    def get_queryset(self):
        return Room.objects.all()


class RoomDetail(DetailView):
    model = Room
    template_name = "test1/room_detail.html"
    context_object_name = "room"


class ItemDetail(DetailView):
    model = Device
    template_name = "test1/item_detail.html"
    context_object_name = "item"


def add_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect("test1")


def edit_object(request, model_name, object_id):
    """Vue générique pour éditer n'importe quel modèle"""
    try:
        model = apps.get_model('test1', model_name)
    except LookupError:
        return render(request, "test1/error.html", {"error": f"Modèle '{model_name}' non trouvé"})

    obj = get_object_or_404(model, pk=object_id)
    form_class = get_generic_form(model)
    next_url = request.GET.get("next", "")

    if request.method == "POST":
        form = form_class(request.POST, instance=obj)
        next_url = request.POST.get("next", "")
        if form.is_valid():
            form.save()
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("test1")
    else:
        form = form_class(instance=obj)

    return render(request, "test1/edit.html", {
        "form": form,
        "object": obj,
        "model_name": model_name,
        "next": next_url,
    })
