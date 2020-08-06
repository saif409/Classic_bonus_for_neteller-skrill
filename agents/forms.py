from django import forms
from .models import test,Agents



class createAgetns(forms.ModelForm):
    phone = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
    address = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    designation = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Designation'}))
    work_place = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Work Place'}))
    country = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Country'}))

    city = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'City'}))
    zip = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'Zip'}))
    state = forms.CharField(required=True, label="",
                             widget=forms.TextInput(attrs={'placeholder': 'State'}))
    author_description = forms.CharField(required=True, label="",
                            widget=forms.TextInput(attrs={'placeholder': 'Author Description'}))

    class Meta:
        model=Agents
        fields=[
            'phone',
            'address',
            'profile_picture',
            'designation',
            'work_place',
            'country',
            'city',
            'zip',
            'state',
            'author_description'

        ]