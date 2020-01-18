from django import forms
from northwind.models import Orders, OrderDetails, Products
from django.db import models
from django.forms import ModelForm

class make_order_form(ModelForm):
        def __init__(self, *args, **kwargs):
            super(make_order_form, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
            for key in self.fields:
                self.fields[key].required = True

        class Meta:
            model = Orders
            fields = ['order_date', 'customer_id', 'employee_id', 'freight', 'ship_via', 'ship_name', 'ship_address', 'ship_city', 'ship_region', 'ship_postal_code', 'ship_country' ]
            DATEPICKER = {
                'type': 'text',
                'class': 'form-control',
                'id': 'datetimepicker1'
            }
            
            widgets = {
                'order_date': forms.DateInput(attrs=DATEPICKER)
            }

 
class add_products(ModelForm):
        def __init__(self, *args, **kwargs):
            super(add_products, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
            for key in self.fields:
                self.fields[key].required = True
            self.fields['product_id'].queryset = Products.objects.filter(discontinued=0)

        class Meta:
            model = OrderDetails
            fields = [ 'product_id', 'quantity', 'discount' ]

       