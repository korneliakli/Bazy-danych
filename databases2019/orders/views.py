from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.forms import formset_factory, inlineformset_factory
from django.db.models import Sum
from northwind.models import Orders as OrdersModel  
from northwind.models import OrderDetails as OrderDetailsModel 
from northwind.models import Products
import decimal
from django.contrib import messages
from .forms import make_order_form, add_products 

def make_order(request):
    order=OrdersModel()
    if request.method == 'POST':
        order_form = make_order_form(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            messages.success(request, f'Succesfully created new order no. {order.order_id}')
            return redirect('add_order_details/' + str(order.order_id) + '/')
    else:
        order_form = make_order_form(instance=order)
    return render(request, 'orders/add_order.html', context = {'order_form': order_form,'order': order})

def add_order_details(request, order_id):
    order_details = OrderDetailsModel()
    if request.method == 'POST':
        order_details_form = add_products(request.POST)
        if order_details_form.is_valid():            
            order_details = order_details_form.save(commit=False)
            prd_id = order_details_form.cleaned_data.get('product_id')
            ordered_product = Products.objects.filter(product_id = prd_id).first()
            in_stock = ordered_product.units_in_stock
            on_order = ordered_product.units_on_order
            if order_details.quantity > (in_stock - on_order):
                messages.warning(request, f'Provided quantity is too large. Available quantity: {in_stock - on_order}')
                return redirect('/orders/add_order_details/' + str(order_id) + '/')
            else:
                order_details.order_id_id = order_id
                order_details.product_id_id = int(order_details.product_id)
                unit_price = Products.objects.filter(product_id = prd_id).first().unit_price
                order_details.unit_price = unit_price
                order_details.discount /= 100
                order_details.save()
                total_price = (unit_price * order_details.quantity * decimal.Decimal(1 - order_details.discount)).quantize(decimal.Decimal('0.01'))
                messages.success(request, f'Products of total value {total_price} EUR added to order no. {order_id}')
                if 'more_products' in request.POST:
                    return redirect('/orders/add_order_details/' + str(order_id) + '/')
                else:
                    return redirect('/orders/' + str(order_id) + '/')
    else:
        order_details_form= add_products(instance=order_details)
        return render(request, 'orders/add_order_details.html', context = {'order_details_form': order_details_form, 'order_id': order_id})


class OrderList(generic.ListView):
    model = OrdersModel
    template_name = 'orders/show_orders.html'
    context_object_name = 'my_orders'
    queryset = OrdersModel.objects.order_by('order_id')
    


class order_detail(generic.DetailView):
        model = OrdersModel
        template_name = 'orders/order_details.html'
        def totalPrice(self):
            total = 0
            for i in self.get_object().orderdetails_set.values():
                total += ( 1 - decimal.Decimal(i.get('discount')) ) * i.get('quantity') * i.get('unit_price')
            return total + self.get_object().freight
        
        def order_detail_view(self, request, primary_key):
            orders = OrdersModel.objects.get(order_id = primary_key)
            return render(request, 'orders/order_details.html', context = {'orders': orders})
