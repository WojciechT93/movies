# Generated by Django 2.2.2 on 2019-06-09 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_comment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set(),
        ),
    ]