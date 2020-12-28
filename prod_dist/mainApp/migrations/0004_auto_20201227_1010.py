# Generated by Django 2.2.13 on 2020-12-27 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_company1_company2_company3_company4'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Company2',
            new_name='Address',
        ),
        migrations.RenameModel(
            old_name='Company4',
            new_name='City',
        ),
        migrations.RenameModel(
            old_name='Company3',
            new_name='Pincode',
        ),
        migrations.RenameField(
            model_name='company1',
            old_name='name',
            new_name='company_name',
        ),
        migrations.AddField(
            model_name='company1',
            name='email',
            field=models.EmailField(default='abc@example.com', max_length=255, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company1',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='company1',
            name='password',
            field=models.CharField(default='Abc123', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]