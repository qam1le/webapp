# Generated by Django 4.2.1 on 2023-12-20 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_system', '0004_remove_mapcreation_upload_model_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlevisionmodel',
            name='labels',
            field=models.JSONField(max_length=1024, null=True),
        ),
    ]
