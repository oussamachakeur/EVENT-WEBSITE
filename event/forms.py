from django import forms 
from django.forms import ModelForm
from .models import Venue , Event



class VenueForm(forms.ModelForm):

    class Meta :
        model = Venue
        #fields='__all__'
        fields=('name','address','zip_code','phone' ,'web' , 'email')

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'web':forms.TextInput(attrs={'class':'form-control'}) ,
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


class EventForm(forms.ModelForm):

    class Meta :
        model = Event
        #fields='__all__'
        fields=('name','date','venue','manager' ,'description' )

        widgets= {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'date':forms.TextInput(attrs={'class':'form-control','type': 'date'}),
            'venue': forms.Select(attrs={'class': 'form-control'}),  
            'manager': forms.Select(attrs={'class': 'form-control'}), 
            'description':forms.TextInput(attrs={'class':'form-control'}) ,
        }

