# Generated by Django 3.1.1 on 2021-06-15 19:07

import auth_api.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.CharField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30)),
                ('mobile_number', models.CharField(blank=True, max_length=10, null=True)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Sub Admin'), (3, 'Distributor'), (4, 'Customer')], null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ShopModel',
            fields=[
                ('shop_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('shop_name', models.CharField(blank=True, max_length=50, null=True)),
                ('shop_address', models.CharField(blank=True, max_length=200, null=True)),
                ('shop_mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('shop_logo', models.CharField(blank=True, max_length=500, null=True)),
                ('shop_active', models.BooleanField(default=False)),
                ('shop_license', models.CharField(blank=True, max_length=7, null=True, unique=True)),
                ('shop_type', models.SmallIntegerField(choices=[(1, 'Eegai Only'), (2, 'Dockt Only'), (3, 'Both Eegai and Dockt')], default=1)),
                ('subscription_type', models.SmallIntegerField(choices=[(1, 'Sub 1'), (2, 'Sub 2')], default=1)),
                ('subscription_start', models.DateTimeField(blank=True, null=True)),
                ('subscription_end', models.DateTimeField(blank=True, null=True)),
                ('shop_address_2', models.CharField(blank=True, max_length=100, null=True)),
                ('shop_address_3', models.CharField(blank=True, max_length=100, null=True)),
                ('gsit', models.CharField(blank=True, max_length=50, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Shop Model',
            },
        ),
        migrations.CreateModel(
            name='SubadminPermisionModel',
            fields=[
                ('manager_permission_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Manager Permision Model',
            },
        ),
        migrations.CreateModel(
            name='SubAdminModel',
            fields=[
                ('sub_admin_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sub_admin_name', models.CharField(blank=True, max_length=20, null=True)),
                ('sub_admin_address', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_admin_mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sub-admin Model',
            },
        ),
        migrations.CreateModel(
            name='ShopPermissionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parmission1', models.BooleanField(default=False)),
                ('parmission2', models.BooleanField(default=False)),
                ('parmission3', models.BooleanField(default=False)),
                ('parmission4', models.BooleanField(default=False)),
                ('parmission5', models.BooleanField(default=False)),
                ('parmission6', models.BooleanField(default=False)),
                ('parmission7', models.BooleanField(default=False)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
            ],
            options={
                'verbose_name': 'Shop Permission Model',
            },
        ),
        migrations.CreateModel(
            name='ForgotTokenModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('expiry_time', models.DateTimeField(blank=True, default=auth_api.models.ForgotTokenModel.now_plus_30)),
                ('forgot_otp', models.PositiveSmallIntegerField()),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Forgot Token',
            },
        ),
        migrations.CreateModel(
            name='DistributorModel',
            fields=[
                ('distributor_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('distributor_name', models.CharField(blank=True, max_length=20, null=True)),
                ('distributor_address', models.CharField(blank=True, max_length=100, null=True)),
                ('distributor_mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Distributor Model',
            },
        ),
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('customer_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('customer_name', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_address_1', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_address_2', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_address_3', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_balance', models.IntegerField(default=0)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer Model',
            },
        ),
        migrations.CreateModel(
            name='AdminModel',
            fields=[
                ('admin_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('admin_name', models.CharField(blank=True, max_length=20, null=True)),
                ('admin_address', models.CharField(blank=True, max_length=100, null=True)),
                ('admin_mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Admin Model',
            },
        ),
        migrations.AddField(
            model_name='account',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth_api.shopmodel'),
        ),
    ]
