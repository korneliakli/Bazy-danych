# Generated by Django 3.0.2 on 2020-01-17 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('northwind', '0002_products_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='product_id',
            field=models.ForeignKey(db_column='product_id', on_delete=django.db.models.deletion.DO_NOTHING, to='northwind.Products'),
        ),
    ]