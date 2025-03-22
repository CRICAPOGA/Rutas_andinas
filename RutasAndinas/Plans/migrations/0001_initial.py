# Generated by Django 5.1.7 on 2025-03-22 16:01

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('category', models.CharField(max_length=30, verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=30, verbose_name='Name')),
                ('description', models.CharField(max_length=1000, verbose_name='Description')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Price')),
                ('hasTransport', models.BooleanField(default=False, verbose_name='Has Transport?')),
                ('hasMeal', models.BooleanField(default=False, verbose_name='Has Meal?')),
                ('hasGuide', models.BooleanField(default=False, verbose_name='Has Guide?')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Plans.categories', verbose_name='Category')),
            ],
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('picture_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('picture', models.ImageField(default=None, upload_to='galery/')),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Plans.plans', verbose_name='Plans')),
            ],
        ),
    ]
