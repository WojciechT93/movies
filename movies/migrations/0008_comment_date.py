# Generated by Django 2.2.2 on 2019-06-09 20:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20190609_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='Date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
