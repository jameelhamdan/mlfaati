# Generated by Django 3.1.5 on 2021-01-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210120_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='content_type',
            field=models.CharField(db_index=True, max_length=144),
        ),
    ]