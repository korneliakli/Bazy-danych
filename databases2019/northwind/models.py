from django.db import models
from django.utils.translation import ugettext as _

class Suppliers(models.Model):
	
	supplier_id = models.AutoField(primary_key=True)
	company_name = models.CharField(max_length=50)
	contact_name = models.CharField(max_length=50, blank=True, null=True)
	contact_title = models.CharField(max_length=40, blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=50,blank=True, null=True)
	region = models.CharField(max_length=40, blank=True, null=True)
	postal_code = models.CharField(max_length=15, blank=True, null=True)	
	country = models.CharField(max_length=20, blank=True, null=True)
	phone = models.CharField(max_length=25, blank=True, null=True)
	fax = models.CharField(max_length=24, blank=True, null=True)
	home_page = models.TextField(blank=True, null=True)

class Category(models.Model):
	objects = models.Manager()
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=50)
	description = models.TextField(blank=True, null=True)
	picture = models.BinaryField(blank=True, null=True)

	def __str__(self):
	 return self.category_name

class Products(models.Model):
	objects = models.Manager()
	product_id = models.AutoField(primary_key=True)
	product_name = models.CharField(max_length=50, blank=False, null=False)
	supplier_id = models.ForeignKey(Suppliers, on_delete=models.CASCADE, blank=True, null=True)
	caregory_id = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	quantity_per_unit = models.CharField(max_length=50, blank=True, null=True)
	unit_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
	units_in_stock = models.SmallIntegerField(blank=True, null=True)
	units_on_order = models.SmallIntegerField(blank=True, null=True)
	reorder_level = models.SmallIntegerField(blank=True, null=True)
	discontinued = models.IntegerField()

	def __str__(self):
		return self.product_name

	def __int__(self):
		return self.product_id

class Region(models.Model):
	region_id = models.AutoField(primary_key=True)
	region_description = models.CharField(max_length=50)

class Territories(models.Model):
	territory_id = models.AutoField(primary_key=True)
	territory_description = models.CharField(max_length=50)
	region_id = models.ForeignKey(Region, on_delete=models.CASCADE)

class Employees(models.Model):
	employee_id = models.AutoField(primary_key=True)
	last_name = models.CharField(max_length=100)
	first_name = models.CharField(max_length=100)
	title = models.CharField(max_length=40, blank=True, null=True)
	title_of_courtesy = models.CharField(max_length=40, blank=True, null=True)
	birth_date = models.DateField(blank=True, null=True)
	hire_date = models.DateField(blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=50, blank=True, null=True)
	region = models.CharField(max_length=40, blank=True, null=True)
	postal_code = models.CharField(max_length=15, blank=True, null=True)
	country = models.CharField(max_length=20, blank=True, null=True)
	home_phone = models.CharField(max_length=25, blank=True, null=True)
	extension = models.CharField(max_length=4, blank=True, null=True)
	photo = models.BinaryField(blank=True, null=True)
	notes = models.TextField(blank=True, null=True)
	reports_to = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
	photo_path = models.CharField(max_length=300, blank=True, null=True)
	territories = models.ManyToManyField(Territories, verbose_name=_('Territories'),db_table='employee_territories',blank=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name

class CustomerDemographics(models.Model):
	customer_type_id = models.AutoField(primary_key=True)
	customer_desc = models.TextField(blank=True, null=True)

class Customers(models.Model):
	customer_id = models.AutoField(primary_key=True)
	company_name =models.CharField(max_length=50)
	contact_name = models.CharField(max_length=50, blank=True, null=True)
	contact_title = models.CharField(max_length=40, blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	city = models.CharField(max_length=50, blank=True, null=True)
	region = models.CharField(max_length=40, blank=True, null=True)
	postal_code = models.CharField(max_length=15, blank=True, null=True)
	country = models.CharField(max_length=20, blank=True, null=True)
	phone = models.CharField(max_length=25, blank=True, null=True)
	fax = models.CharField(max_length=24, blank=True, null=True)
	customer_customer_demo = models.ManyToManyField(CustomerDemographics, verbose_name=_('Customer customer demo'),db_table='customer_customer_demo',blank=True)

	def __str__(self):
		return self.company_name

class Shippers(models.Model):
	shipper_id = models.AutoField(primary_key=True)
	company_name = models.CharField(max_length=50)
	phone = models.CharField(max_length=25, blank=True, null=True)

	def __str__(self):
	 return self.company_name

class Orders(models.Model):
	objects = models.Manager()
	order_id = models.AutoField(primary_key=True)
	customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, blank=True, null=True)
	employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, blank=True, null=True)
	order_date = models.DateField(blank=True, null=True)
	required_date = models.DateField(blank=True, null=True)
	shipped_date = models.DateField(blank=True, null=True)
	ship_via = models.ForeignKey(Shippers, on_delete=models.CASCADE, blank=True, null=True)
	freight = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
	ship_name = models.CharField(max_length=50, blank=True, null=True)
	ship_address = models.CharField(max_length=100, blank=True, null=True)
	ship_city = models.CharField(max_length=50, blank=True, null=True)
	ship_region = models.CharField(max_length=40, blank=True, null=True)
	ship_postal_code = models.CharField(max_length=15, blank=True, null=True)
	ship_country = models.CharField(max_length=20, blank=True, null=True)
	order_details = models.ManyToManyField(Products,verbose_name=_('Products'),blank=True,through='OrderDetails')
	
	class Meta:
		managed = False	
		db_table = 'northwind_orders'

class OrderDetails (models.Model):
	order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
	product_id = models.ForeignKey('Products', models.DO_NOTHING, db_column='product_id')
	unit_price = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
	quantity = models.SmallIntegerField()
	discount = models.FloatField()
