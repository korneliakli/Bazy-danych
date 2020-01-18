from django import forms
from django.db import models
from northwind.models import Category
from django.forms import ModelForm

class ReportForm(forms.Form):

        category = forms.ModelChoiceField(Category.objects.all(), empty_label='-------')

        DATEPICKER = {
            'type': 'text',
            'class': 'form-control',
            'id': 'datetimepicker1'
        }
            
        startdate = forms.DateField(
                widget = forms.DateInput(attrs=DATEPICKER)
        )
        
        DATEPICKER2 = {
            'type': 'text',
            'class': 'form-control ',
            'id': 'datetimepicker2'
        }

        enddate = forms.DateField(
                widget = forms.DateInput(attrs=DATEPICKER2)
        )

        def __init__(self, *args, **kwargs):
            super(ReportForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
            for key in self.fields:
                self.fields[key].required = True