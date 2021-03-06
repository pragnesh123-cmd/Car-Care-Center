# Generated by Django 3.0.5 on 2021-02-23 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CCC', '0005_auto_20210222_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='post_name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='job_apply',
            name='post_name',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='CCC.post_name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job_desc',
            name='post_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CCC.post_name'),
        ),
    ]
