"""
Formularze dla aplikacji `doggs`.

Zawiera:
- `DogForm`: formularz dodawania/edycji psa z edytorem treści (CKEditor)
- `ReviewForm`: formularz recenzji psa
"""

from django.forms import ModelForm
from .models import Dog, Review
from django import forms

from ckeditor.widgets import CKEditorWidget
from django import forms


class DogForm(ModelForm):
    """
    Formularz Django do tworzenia/edycji psa.

    Wyłącza pole `owner`, dodaje klasę CSS do każdego pola.
    """
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Dog
        fields = ['name', 'description', 'wiki_link', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(DogForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update({'class': 'input', 'placeholder': 'Add name'})
        for name, field in self.fields.items():
            # if name == "description":
            field.widget.attrs.update({'class': 'input'})

class ReviewForm(ModelForm):
    """
    Formularz recenzji psa – głos i treść.

    Używany w widoku szczegółów psa.
    """
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote',

        }
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs.update({'class': 'input', 'placeholder': 'Add name'})
        for name, field in self.fields.items():
            # if name == "description":
            field.widget.attrs.update({'class': 'input'})