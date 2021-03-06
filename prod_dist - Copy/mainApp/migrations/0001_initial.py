# Generated by Django 2.2.13 on 2021-02-04 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('state', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('company_name', models.CharField(max_length=20, unique=True)),
                ('gst_number', models.CharField(max_length=20, unique=True)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.CharField(max_length=15)),
                ('gst_number', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pincode',
            fields=[
                ('pincode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.City')),
            ],
            options={
                'unique_together': {('pincode', 'city')},
            },
        ),
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile', models.CharField(max_length=15)),
                ('gst_number', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Address')),
                ('distributor_retailers', models.ManyToManyField(db_table='distributes', to='mainApp.Retailer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_distributor_price', models.FloatField()),
                ('product_distributor_margin', models.FloatField()),
                ('product_retailer_price', models.FloatField()),
                ('product_retailer_margin', models.FloatField()),
                ('product_mrp', models.FloatField()),
                ('product_discount', models.FloatField()),
                ('cg_gst', models.FloatField()),
                ('sg_gst', models.FloatField()),
                ('total_tax', models.FloatField()),
                ('hsn_code', models.CharField(default='', max_length=50)),
                ('fssai_number', models.CharField(blank=True, max_length=50, null=True)),
                ('product_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Company')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='company_distributors',
            field=models.ManyToManyField(db_table='supplies', to='mainApp.Distributor'),
        ),
        migrations.AddField(
            model_name='address',
            name='pincode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.Pincode'),
        ),
    ]
