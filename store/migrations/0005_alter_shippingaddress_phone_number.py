# Generated by Django 5.0.3 on 2024-05-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_shippingaddress_state_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='phone_number',
            field=models.CharField(max_length=9, null=True),
        ),
    ]
