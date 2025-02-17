# Generated by Django 3.2.12 on 2022-03-05 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_auto_20220226_1212'),
        ('demand', '0006_auto_20220305_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=models.ManyToManyField(related_name='category_demand', to='category.Category'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='service',
            field=models.ManyToManyField(related_name='service_demand', to='category.Service'),
        ),
    ]
