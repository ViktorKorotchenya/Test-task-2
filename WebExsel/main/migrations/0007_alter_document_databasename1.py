# Generated by Django 4.1 on 2022-08-25 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_databasename_document_databasename1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='databasename1',
            field=models.FileField(upload_to='db_files/'),
        ),
    ]
