# Generated by Django 3.1.1 on 2021-06-15 19:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItemModel',
            fields=[
                ('orderitem_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('item_price', models.FloatField()),
                ('item_gst_price', models.FloatField()),
                ('item_quantity', models.IntegerField()),
                ('item_status', models.PositiveSmallIntegerField(choices=[(1, 'Un-billed'), (2, 'Billed')], default=1, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Order Item Model',
            },
        ),
        migrations.CreateModel(
            name='TermsandConditionsModel',
            fields=[
                ('tc_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('terms', models.CharField(default=None, max_length=500)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Terms Model',
            },
        ),
        migrations.CreateModel(
            name='RandomItemModel',
            fields=[
                ('randomitem_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('product_gst', models.IntegerField(blank=True, default=None, null=True)),
                ('product_price', models.FloatField(blank=True, default=None, null=True)),
                ('product_quantity', models.IntegerField(default=None)),
                ('item_price', models.FloatField()),
                ('item_gst_price', models.FloatField()),
                ('item_status', models.PositiveSmallIntegerField(choices=[(1, 'Un-billed'), (2, 'Billed')], default=1, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Random Item Model',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('product_code', models.CharField(blank=True, max_length=50, null=True)),
                ('product_name', models.CharField(blank=True, max_length=100, null=True)),
                ('product_stock', models.IntegerField(blank=True, null=True)),
                ('product_gst', models.FloatField(blank=True, default=0, null=True)),
                ('product_vendor_price', models.FloatField(blank=True, null=True)),
                ('product_mrp_price', models.FloatField(blank=True, null=True)),
                ('product_value', models.CharField(blank=True, max_length=50, null=True)),
                ('product_type', models.SmallIntegerField(blank=True, choices=[(1, 'Gram'), (2, 'Kilo Gram'), (3, 'Piece'), (4, 'Box / Packets'), (5, 'Litre'), (6, 'Milli Litre')], default=1, null=True)),
                ('product_template', models.SmallIntegerField(blank=True, choices=[(1, 'Product - Expiry'), (2, 'Product - Non-Expiry'), (3, ' v 2')], default=1, null=True)),
                ('product_available', models.BooleanField(default=True)),
                ('product_expiry', models.DateField(blank=True, null=True)),
                ('time_stamp', models.DateTimeField(auto_now=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Product Model',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('order_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('order_no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('order_price', models.FloatField(blank=True, null=True)),
                ('order_gst_price', models.FloatField(blank=True, null=True)),
                ('order_discounted_price', models.FloatField(blank=True, null=True)),
                ('order_discount', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('order_balance', models.PositiveIntegerField(blank=True, null=True)),
                ('order_status', models.PositiveSmallIntegerField(choices=[(1, 'Fully Payment'), (2, 'Partial Payment')], default=1, null=True)),
                ('order_payment', models.PositiveSmallIntegerField(choices=[(1, 'Online'), (2, 'Cash'), (2, 'Not Paid')], default=1, null=True)),
                ('account_type', models.PositiveSmallIntegerField(choices=[(1, 'Billed'), (2, 'Not Billed'), (2, 'Temp')], default=1, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_api.customermodel')),
                ('order_items', models.ManyToManyField(to='core_api.OrderItemModel')),
                ('random_items', models.ManyToManyField(to='core_api.RandomItemModel')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Order Model',
            },
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_api.productmodel'),
        ),
        migrations.AddField(
            model_name='orderitemmodel',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel'),
        ),
        migrations.CreateModel(
            name='BankdetailModel',
            fields=[
                ('detail_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bank_name', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('bank_account_no', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('bank_branch', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('bank_ifsc', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('UPI_id', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Bank Detail Model',
            },
        ),
    ]
