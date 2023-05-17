# Generated by Django 3.2.18 on 2023-05-05 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cameras', '0003_camera_cameravideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.TimeField(auto_created=True)),
                ('camera_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cameras.camera')),
            ],
        ),
    ]