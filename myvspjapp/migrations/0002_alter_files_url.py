# Generated by Django 4.0.4 on 2022-05-29 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myvspjapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='url',
            field=models.FileField(upload_to='filevault/', verbose_name=''),
        ),
    ]
