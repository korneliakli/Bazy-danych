# Stworzenie modeli w języku Python

Aby stworzyć model tabeli w języku python należy zdefiniować klasę oraz poszczególne obiekty (kolumny w bazie).
Jak zaznaczono na przykładzie poniżej, gdzie 
Category - nazwa tabeli
category_id, category_name, etc. nazwy kolumn
Typ pola:
- AutoField - pole autowypełniające, zazwyczaj z kluczem głównym
- CharField - pole typu char
TextField - pole typu string
BinaryField - pole typu bool
Właściwości pola:
primary_key - klucz główny
max_length - maksymalna długość pola
null - czy puste pole
'''
class Category(models.Model):
  objects = models.Manager()
  category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	picture = models.BinaryField(blank=True, null=True)

Oczywiście może być wiele właściwości pola zdefiniowanych

Na podstawie wyżej wymienionych class robimy migrację do bazy danych Postgres


Widoki
W widokach zamówień definiujemy poszczególne widoki, które wypełniamy oraz definiujemy warunki brzegowe, które następnie migrują do bazy danych.
W order_form.is_valid() sprawdzamy, czy format danych się zgadza. A nastepnie przekazujemy w order = order_form.save(commit=False) informacje do modelu, a następnie /w order.save()/ do bazy danych.

def make_order(request):
    order=OrdersModel()
    if request.method == 'POST':
        order_form = make_order_form(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()
            messages.success(request, f'Succesfully created new order no. {order.order_id}')
            return redirect('add_order_details/' + str(order.order_id) + '/')

Poniżej kolejny przykład, który różni się od poprzedniego pobieraniem informacji z danych.
W totalPrice wyliczana jest sumaryczna kwota za wszystkie produkty w zamówieniu. Jest to prosta pętla, która mnoży ilość elementów, zniżkę oraz cenę jednostkową. A następnie sumuje.
W render system pobiera informacje z bazy danych, a w context przekazuje zmienne.
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

Kolejny przykład poniżej, gdzie:
1. wpierw definiujemy id zamówienia
2.definiujemy id produktu
3. pobieramy unit_price z tabeli
4. -------------------||-------------------
5. definiujemy przedział discount
6. oraz przekazujemy dane do Bazy danych

>                order_details.order_id_id = order_id
>                order_details.product_id_id = int(order_details.product_id)
>                unit_price = Products.objects.filter(product_id = prd_id).first().unit_price
>                order_details.unit_price = unit_price
>                order_details.discount /= 100
>                order_details.save()

W poniższym przykładzie jeszcze jest sposób ustanawiania kolejności po order_id

>    queryset = OrdersModel.objects.order_by('order_id')



Northwind - Template - Orders

Poniżej istnieje połączenie z wcześniej wymienionymi formami z wyświetlanymi elementami na hoście.
{% - programowane elementy
{{ - odwołanie do połaczeń
Na przykład poniżej:
	form action - odpowiada za bezpieczeństwo
a {{ order_details_form.management_form }} odwołuje się do tego elementu w modelu
submit - dodanie przycisku, który przesyła dane za pomocą POST
Przykład:
<div>
<form action="/orders/add_order_details/{{order_id}}/" method="post">
	{% csrf_token %}
	{{ order_details_form.management_form }}
<table>
<div class="form-group col-md-11">
	{{ order_details_form.as_p }}
</div>
</table>

	<input type="submit" name="more_products" value="Add more products" class="btn btn-primary col-md-3" />
	<input type="submit" name="submit" value="Submit" class="btn btn-primary col-md-3" />
</form>
</div>


Defniniowanie pliku urls.py w Zamówieniu
Polega na zmapowaniu poszczególnych elementów, w którym odnoszą się do ścieżki.
Na przykład w  path('add_order_details/<int:order_id>/', views.add_order_details,name="add-order-details") przypisujemy ścieżce add_order_details widok o nazwie add_order_details, a w <int:order_id> definiujemy dopuszczalne wartości (np. numer zamówienia, który musi mieć wartość integer).

urlpatterns = [
    path('', views.make_order, name="make-order"),
    path('add_order_details/<int:order_id>/', views.add_order_details,name="add-order-details"),
    path('<int:pk>/', views.order_detail.as_view(), name='order-detail'),
    path('show_orders/', views.OrderList.as_view(), name="show-orders"),
]


Tworzenie raportów
Tworzenie raportów przebiega, jak w przykładzie poniżej, w którym definiujemy klasę o nazwie raportu. W Products.objects.annotate następuje agregacja. Ta długa funkcja która sumuje iloczyn poszczególneych elementy w Zamówieniach (Ilość, zniżkę oraz cenę jedn.).

def generate_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            startdate = form.cleaned_data['startdate']
            enddate = form.cleaned_data['enddate']
            products = Products.objects.annotate(product_value=Sum(ExpressionWrapper(F('orders__orderdetails__quantity') * F('orders__orderdetails__unit_price') * (1 - F('orders__orderdetails__discount')), output_field=FloatField()),filter=Q(orders__orderdetails__product_id__caregory_id_id=Category.objects.get(category_name=category), orders__order_date__range=(startdate, enddate)))).filter(product_value__gt=0).order_by('product_name')
            

Tworzenie form
Poniżej jest załączony przykład, w którym definiujemy formę make_order., która dziedziczy po ModelForm. W pętlach for następuje wyświetlenie elementów zamieszczonych w liście. W praktyce daje to funkcjonalność po kliknięciu na polu pokazaniu listy z elementami możliwymi do wybrania.
W klasie meta wybieramy jaki model /Orders/, jakie pola z modelu będą brane oraz poniżej w widget typ wyświetlania daty. 

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

Poniżej przykład też sposób filtrowania elementów typu DESC:

            self.fields['product_id'].queryset = Products.objects.filter(discontinued=0)

