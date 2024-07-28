from django import forms

from blog.models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
