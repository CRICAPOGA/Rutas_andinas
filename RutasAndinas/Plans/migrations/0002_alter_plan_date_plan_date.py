<<<<<<< HEAD
# Generated by Django 5.1.6 on 2025-04-01 00:07
=======
# Generated by Django 5.1.6 on 2025-03-31 22:20
>>>>>>> origin/develop-Cristian

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Plans', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan_date',
            name='plan_date',
            field=models.DateField(verbose_name='Date'),
        ),
    ]
