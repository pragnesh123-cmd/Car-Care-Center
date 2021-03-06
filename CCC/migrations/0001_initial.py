# Generated by Django 3.0.5 on 2021-02-18 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('msg', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='cus_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=40)),
                ('number', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=40)),
                ('brand', models.CharField(max_length=40)),
                ('model', models.CharField(max_length=40)),
                ('problem', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now=True)),
                ('cost', models.IntegerField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Repairing', 'Repairing'), ('Repairing Done', 'Repairing Done'), ('Released', 'Released')], default='Pending', max_length=40, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30)),
                ('lname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=7)),
                ('address', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=50)),
                ('msg', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='mechanic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=10)),
                ('gender', models.CharField(max_length=20)),
                ('designation', models.CharField(max_length=20)),
                ('salary', models.FloatField(max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='paytm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ORDER_ID', models.CharField(max_length=50)),
                ('TXN_AMOUNT', models.CharField(max_length=30)),
                ('BANKTXNID', models.CharField(max_length=50)),
                ('BANKNAME', models.CharField(max_length=50)),
                ('TXNDATE', models.DateField(auto_now=True)),
                ('STATUS', models.CharField(choices=[('TXN_SUCCESS', 'TXN_SUCCESS'), ('TXN_FAIL', 'TXN_FAIL')], default='TXN_FAIL', max_length=30)),
                ('Cus_Request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CCC.cus_request')),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CCC.customer')),
            ],
        ),
        migrations.AddField(
            model_name='cus_request',
            name='Customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CCC.customer'),
        ),
        migrations.AddField(
            model_name='cus_request',
            name='Mechanic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CCC.mechanic'),
        ),
        migrations.CreateModel(
            name='apply_leave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=100)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=40, null=True)),
                ('admin_reason', models.CharField(max_length=100)),
                ('Mechanic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CCC.mechanic')),
            ],
        ),
    ]
