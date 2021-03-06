# Generated by Django 3.1.1 on 2021-06-25 21:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0002_auto_20210621_2053'),
        ('core_api', '0004_productmodel_product_mrp_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='customer',
        ),
        migrations.CreateModel(
            name='CoupounModel',
            fields=[
                ('coupoun_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('coupoun_code', models.CharField(blank=True, max_length=10, null=True)),
                ('coupoun_description', models.CharField(blank=True, max_length=100, null=True)),
                ('coupoun_min_value', models.FloatField()),
                ('coupoun_discount', models.FloatField()),
                ('coupoun_max_discount', models.FloatField()),
                ('coupoun_limit', models.IntegerField()),
                ('coupoun_expiry', models.DateTimeField()),
                ('coupoun_type', models.PositiveSmallIntegerField(choices=[(1, 'Type1'), (2, 'Type2')], default=1, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Coupoun Model',
            },
        ),
    ]
