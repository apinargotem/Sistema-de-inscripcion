# Generated by Django 4.1 on 2022-09-24 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestión_académica', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscripcion',
            name='Identificacion',
        ),
    ]
