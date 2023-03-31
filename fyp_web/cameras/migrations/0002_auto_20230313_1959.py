# Generated by Django 3.2.16 on 2023-03-13 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='cameraClose',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='LEFT_CAMERA', to='cameras.camera'),
        ),
        migrations.AddField(
            model_name='camera',
            name='cameraClose2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Right_Camera', to='cameras.camera'),
        ),
    ]