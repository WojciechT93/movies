# Generated by Django 2.2.2 on 2019-06-09 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20190608_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='Actors',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Awards',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='BoxOffice',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='DVD',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Director',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Genre',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='ImdbID',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='ImdbRating',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='ImdbVotes',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Language',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Metascore',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Plot',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Poster',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Production',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Rated',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Released',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Runtime',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Type',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Writer',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='Year',
            field=models.IntegerField(blank=True),
        ),
    ]