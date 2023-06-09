# Generated by Django 4.2.1 on 2023-06-05 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_system', '0003_imageuploadmodel_lat_imageuploadmodel_lon'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleVisionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50, null=True)),
                ('coordinates', models.CharField(max_length=50, null=True)),
                ('score', models.DecimalField(decimal_places=15, max_digits=30, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
