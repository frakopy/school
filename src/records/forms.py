from django import forms
from .models import Record


class EditRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ["present", "comments"]
        exclude = ("student", "schedule", "course")
        widgets = {
            "present": forms.Select(
                attrs={"class": "form-select"},
                choices=[("unknown", "Desconocido"), ("true", "Sí"), ("false", "No")],
            ),
            "comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "cols": 40}
            ),
        }

class StudentRecordUpdateForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = ["present", "comments", "start_date"]
        exclude = ("student", "schedule", "course")
        widgets = {
            "present": forms.Select(
                attrs={"class": "form-select"},
                choices=[("unknown", "Desconocido"), ("true", "Sí"), ("false", "No")],
            ),
            "comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "cols": 40}
            ),
            "start_date": forms.DateInput(attrs={"class": "form-control"}),
        }

        labels = {
            "present": "Presente",
            "comments": "Observaciones",
            "start_date": "Fecha de inicio (dia/mes/año)"
        }  