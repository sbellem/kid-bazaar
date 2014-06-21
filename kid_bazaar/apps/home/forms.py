from django import forms

from . import models


class ItemForm(forms.ModelForm):
    class Meta:
        model = models.Item
        fields = ('name', 'pic', 'description', 'category', 'price', 'age_from_years', 'age_from', 'age_to_years', 'age_to')
    name = forms.CharField(max_length=100)
    description = forms.CharField(required=False, widget=forms.Textarea)
    category = forms.CharField(max_length=100, required=False)
    price = forms.DecimalField(required=False)
    age_from_years = forms.IntegerField(min_value=0, required=False, label=u'Using from age of (years)')
    age_from = forms.IntegerField(min_value=0, required=False, label=u'Using from age of (months)')
    age_to_years = forms.IntegerField(min_value=0, required=False, label=u'Using from age of (years)')
    age_to = forms.IntegerField(min_value=0, required=False, label=u'Using from age of (months)')


class KidForm(forms.ModelForm):
    class Meta:
        model = models.Kid
        fields = ('name', 'birthday', 'sex')
    name = forms.CharField(max_length=100, required=False)
    birthday = forms.DateField()
    sex = forms.CharField(required=False)
