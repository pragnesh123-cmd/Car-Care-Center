# Generated by Django 3.0.5 on 2021-02-19 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CCC', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cus_request',
            name='payment_status',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
