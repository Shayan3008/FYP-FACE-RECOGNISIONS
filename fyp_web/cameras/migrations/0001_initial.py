# Generated by Django 3.2.16 on 2023-03-11 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coordinates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cameraLocation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='coordinates.coordinates')),
            ],
        ),
    ]
