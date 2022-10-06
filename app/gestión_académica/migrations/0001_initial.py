# Generated by Django 4.1 on 2022-09-24 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('Codigo', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=200, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('Codigo', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=100, verbose_name='Curso')),
                ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('Horas', models.PositiveSmallIntegerField()),
                ('Valor', models.FloatField()),
                ('Imagen', models.ImageField(null=True, upload_to='cursos')),
                ('Descripcion', models.TextField(max_length=10000)),
                ('Fecha_Inicio', models.DateTimeField()),
                ('Estado', models.BooleanField(default=True)),
                ('Id_moodle', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Identidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cedula', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'verbose_name': 'Identidad',
                'verbose_name_plural': 'Identidades',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=100)),
                ('codigo_estado', models.CharField(max_length=100)),
                ('total_de_la_compra', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('apellido_cliente', models.CharField(max_length=100)),
                ('correo_cliente', models.EmailField(max_length=100)),
                ('direccion_cliente', models.CharField(max_length=100)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, verbose_name='nombre del usuario')),
                ('uid', models.CharField(max_length=500)),
                ('room_name', models.CharField(max_length=150, verbose_name='nombre de la sala')),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaInscripcion', models.DateTimeField(auto_now_add=True)),
                ('Id_moodle', models.IntegerField(blank=True, default=0, null=True)),
                ('Identificacion', models.TextField(blank=True, null=True)),
                ('Curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='gestión_académica.curso')),
                ('Pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='gestión_académica.pago')),
            ],
            options={
                'verbose_name': 'Inscripción',
                'verbose_name_plural': 'Inscripciones',
            },
        ),
    ]
