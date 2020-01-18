from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import DateTimeField, ExpressionWrapper, F, Sum, Q, FloatField
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.forms import formset_factory, inlineformset_factory
from django.views.generic.edit import FormView
from django.db.models import Sum
from django.contrib import messages

from northwind.models import Orders, OrderDetails, Category, Products
from .forms import ReportForm

def generate_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            startdate = form.cleaned_data['startdate']
            enddate = form.cleaned_data['enddate']
            products = Products.objects.annotate(product_value=Sum(ExpressionWrapper(F('orders__orderdetails__quantity') * F('orders__orderdetails__unit_price') * (1 - F('orders__orderdetails__discount')), output_field=FloatField()),filter=Q(orders__orderdetails__product_id__caregory_id_id=Category.objects.get(category_name=category), orders__order_date__range=(startdate, enddate)))).filter(product_value__gt=0).order_by('product_name')
            messages.success(request, f'Succesfully generated report for {category} category')
            return render(request, 'reports/generated_report.html', context = { 'results' : products, 'category' : category })
    else:
        form  = ReportForm()
    return render(request, 'reports/report.html', context = {'form':form})