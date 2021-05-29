# Generated by Django 3.2.3 on 2021-05-29 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_user_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(max_length=150)),
                ('image', models.ImageField(upload_to='')),
                ('date', models.DateField()),
                ('visit_amount', models.IntegerField()),
            ],
        ),
    ]