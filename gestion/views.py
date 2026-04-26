from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.apps import apps
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

# Create your views here.
from django.views.generic import ListView, DetailView

from Refu5Ge.decorators import group_required
from core.models import *
from .forms import *

DeviceAttributeFormSet = inlineformset_factory(
    Device,
    DeviceAttribute,
    fields=("key", "value"),
    extra=0,
    can_delete=True,
)


class AllRooms(LoginRequiredMixin, ListView):
    model = Room
    template_name = "gestion/allRooms.html"

    def get_queryset(self):
        return Room.objects.all()


class RoomDetail(LoginRequiredMixin, DetailView):
    model = Room
    template_name = "gestion/room_detail.html"
    context_object_name = "room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from rapports.views import get_monthly_device_report

        context["monthly_report"] = get_monthly_device_report(self.object)
        return context

class ItemDetail(LoginRequiredMixin,DetailView):
    model = Device
    template_name = "gestion/item_detail.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["back_url"] = (
            self.request.GET.get("next")
            or self.request.META.get("HTTP_REFERER")
            or reverse("all_rooms")
        )
        return context




@group_required("manager")
def room_device_add(request, pk):
    room = get_object_or_404(Room, pk=pk)
    device = Device.objects.create(room=room, name="", type="")
    edit_url = reverse("edit_object", kwargs={"model_name": "Device", "object_id": device.id})
    next_url = reverse("room_detail", kwargs={"pk": pk})
    return redirect(f"{edit_url}?next={next_url}")


# TODO: gerer le annuler lors de création d'objet
@group_required("manager")
def edit_object(request, model_name, object_id):
    """Vue générique pour éditer n'importe quel modèle"""
    try:
        model = apps.get_model('core', model_name)
    except LookupError:
        return render(request, "gestion/error.html", {"error": f"Modèle '{model_name}' non trouvé"})
    obj = get_object_or_404(model, pk=object_id)
    form_class = get_generic_form(model)
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER", "")
    is_device = model == Device
    attr_formset = None

    if request.method == "POST":
        form = form_class(request.POST, instance=obj)
        next_url = request.POST.get("next") or next_url
        if is_device:
            attr_formset = DeviceAttributeFormSet(request.POST, instance=obj, prefix="attrs", queryset=obj.attributes.exclude(key="state"))

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
            return redirect("all_rooms")
    else:
        form = form_class(instance=obj)
        if is_device:
            attr_formset = DeviceAttributeFormSet(instance=obj, prefix="attrs", queryset=obj.attributes.exclude(key="state"))

    return render(request, "gestion/edit.html", {
        "form": form,
        "attr_formset": attr_formset,
        "object": obj,
        "model_name": model_name,
        "next": next_url,
    })





@require_POST
@group_required("manager")
def toggle_device(request, pk):
    d = get_object_or_404(Device, pk=pk)
    d.state = not d.state
    d.save(update_fields=["state"])
    DeviceLogActivation.objects.create(device=d, state=d.state,)
    return redirect(request.POST.get("next") or "item_detail", pk=d.pk)
