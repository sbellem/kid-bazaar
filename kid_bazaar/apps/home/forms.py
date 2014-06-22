from django import forms
from cloudinary.forms import CloudinaryFileField

from . import models


CATEGORIES = (
    (u'Education and Toys', u'Education and Toys'),
    (u'Clothes and Linens', u'Clothes and Linens'),
    (u'Feeding equipment', u'Feeding equipment'),
    (u'Furniture', u'Furniture'),
    (u'Others', u'Others'),
    )

SEX = (
    (u'FEMALE', 'Girl'),
    (u'MALE', 'Boy'),
)


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ('name', 'pic', 'description', 'category', 'price', 'age_from_years', 'age_from', 'age_to_years', 'age_to')
    pic = CloudinaryFileField()
    name = forms.CharField(max_length=100)
    description = forms.CharField(required=False, widget=forms.Textarea)
    category = forms.ChoiceField(required=False, choices=CATEGORIES)
    price = forms.DecimalField(required=False)
    age_from_years = forms.IntegerField(min_value=0, required=False, label=u'Using from age of (years)')
    age_from = forms.IntegerField(min_value=0, required=False, label=u'Using from age of (months)')
    age_to_years = forms.IntegerField(min_value=0, required=False, label=u'Using until age of (years)')
    age_to = forms.IntegerField(min_value=0, required=False, label=u'Using until age of (months)')


class KidForm(forms.ModelForm):
    class Meta:
        model = models.Kid
        fields = ('name', 'pic', 'birthday', 'sex')
    pic = CloudinaryFileField()
    name = forms.CharField(max_length=100, required=False)
    birthday = forms.DateField(widget=forms.DateInput)
    sex = forms.ChoiceField(required=False, choices=SEX)
