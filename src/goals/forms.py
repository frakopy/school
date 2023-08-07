from django import forms
from .models import Goals


class CreateGoalForm(forms.ModelForm):

    class Meta:

        model = Goals
        fields = ["name", "classroom"]
        exclude = ("teacher", "course")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control text-center",
                    "placeholder": "Escriba el nombre del objetivo",
                }
            ),
            "classroom": forms.Select(
                attrs={"class": "form-select text-center"},
            ),
        }

        labels = {
            "name": "",
            "classroom": "",
        }

    def __init__(self, teacher, *args, **kwargs):
        super().__init__(*args, **kwargs)
        classrooms = teacher.classroom_set.all()
        classrooms_options = [(c.pk, c.level.short_name + "-" + c.code) for c in classrooms]
        self.fields["classroom"].widget.choices = classrooms_options