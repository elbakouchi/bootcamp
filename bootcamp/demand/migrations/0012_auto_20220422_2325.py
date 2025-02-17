# Generated by Django 3.2.12 on 2022-04-22 23:25

import bootcamp.custom
from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0011_alter_demand_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demand',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(validators=[bootcamp.custom.word_counter_validator], verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='has_revision',
            field=models.BooleanField(default=False, verbose_name="N'est pas en attente"),
        ),
        migrations.AlterField(
            model_name='demand',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Vérifié'),
        ),
    ]
