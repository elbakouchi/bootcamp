# Generated by Django 3.2.12 on 2022-03-23 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0009_auto_20220320_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='has_revision',
            field=models.BooleanField(default=False, verbose_name='Vérifié'),
        ),
    ]
