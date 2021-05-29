# Generated by Django 3.2.3 on 2021-05-18 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(blank=True, max_length=30, unique=True)),
                ('email', models.EmailField(blank=True, max_length=60, verbose_name='email')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Жанры')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('paper_count', models.IntegerField(blank=True)),
                ('rating', models.CharField(blank=True, max_length=50)),
                ('rating_count', models.IntegerField(blank=True)),
                ('status', models.CharField(blank=True, max_length=50)),
                ('category', models.IntegerField(blank=True)),
                ('photo', models.ImageField(blank=True, upload_to='')),
                ('short_description', models.TextField(blank=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.genre', verbose_name='Жанр')),
            ],
        ),
    ]
