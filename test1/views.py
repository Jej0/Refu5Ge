from datetime import date

from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.apps import apps
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

# Create your views here.
from django.views.generic import ListView, DetailView

from Refu5Ge.decorators import group_required
from .models import *
from .forms import *


DeviceAttributeFormSet = inlineformset_factory(
    Device,
    DeviceAttribute,
    fields=("key", "value"),
    extra=0,
    can_delete=True,
)


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


def room_device_add(request, pk):
    room = get_object_or_404(Room, pk=pk)
    device = Device.objects.create(room=room, name="", type="")
    edit_url = reverse("edit_object", kwargs={"model_name": "Device", "object_id": device.id})
    next_url = reverse("room_detail", kwargs={"pk": pk})
    return redirect(f"{edit_url}?next={next_url}")


def add_test(request):
    if request.method == "POST":
        form = TestForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect("test1")

@group_required("avancé")
def edit_object(request, model_name, object_id):
    """Vue générique pour éditer n'importe quel modèle"""
    try:
        model = apps.get_model('test1', model_name)
    except LookupError:
        return render(request, "test1/error.html", {"error": f"Modèle '{model_name}' non trouvé"})

    obj = get_object_or_404(model, pk=object_id)
    form_class = get_generic_form(model)
    next_url = request.GET.get("next", "")
    is_device = model == Device
    attr_formset = None

    if request.method == "POST":
        form = form_class(request.POST, instance=obj)
        next_url = request.POST.get("next", "")
        if is_device:
            attr_formset = DeviceAttributeFormSet(request.POST, instance=obj, prefix="attrs")

        form_ok = form.is_valid()
        attrs_ok = attr_formset.is_valid() if attr_formset is not None else True

        if form_ok and attrs_ok:
            saved_obj = form.save()
            if attr_formset is not None:
                attr_formset.instance = saved_obj
                attr_formset.save()
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("test1")
    else:
        form = form_class(instance=obj)
        if is_device:
            attr_formset = DeviceAttributeFormSet(instance=obj, prefix="attrs")

    return render(request, "test1/edit.html", {
        "form": form,
        "attr_formset": attr_formset,
        "object": obj,
        "model_name": model_name,
        "next": next_url,
    })
