from django import forms
from northwind.models import Suppliers

class search_form(forms.Form):

    def __init__(self, *args, **kwargs):
        super(search_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    name = forms.CharField(label='Search')


class add_supplier_form(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(add_supplier_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Suppliers
        fields = ['supplier_id', 'company_name', 'contact_name', 'contact_title', 'address', 'city', 'region', 'postal_code', 'country', 'phone', 'fax', 'home_page']