from django import forms
from .models import ToDoItem, Test, Device

class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['text', 'due_date']


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = "__all__"  # Inclut tous les champs (title, value)


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        # room set in view from URL pk
        fields = ["name", "type"]


def get_generic_form(model_class):
    """Génère un formulaire générique pour n'importe quel modèle"""
    class GenericForm(forms.ModelForm):
        class Meta:
            model = model_class
            fields = "__all__"
    return GenericForm
