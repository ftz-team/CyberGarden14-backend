# Generated by Django 3.2.3 on 2021-05-29 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_collector_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='collector',
            name='type',
            field=models.CharField(blank=True, choices=[('general', 'Общего назначения'), ('plastic', 'Для пластика'), ('glass', 'Для стекла'), ('paper', 'Для бумаги'), ('batteries', 'Для батареек')], max_length=100, null=True),
        ),
    ]