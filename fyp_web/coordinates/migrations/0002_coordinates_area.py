# Generated by Django 3.2.16 on 2023-03-14 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('area', '0001_initial'),
        ('coordinates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordinates',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='area.area'),
        ),
    ]
