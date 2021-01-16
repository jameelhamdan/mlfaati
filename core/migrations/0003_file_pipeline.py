# Generated by Django 3.1.5 on 2021-01-16 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0001_initial'),
        ('core', '0002_file_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='pipeline',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='processing.pipeline'),
        ),
    ]