# Generated by Django 3.2.12 on 2022-03-23 23:48

import django.core.validators
from django.db import migrations, models
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20220320_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(validators=[django.core.validators.MaxLengthValidator(100)], verbose_name='Contenu'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1, verbose_name='État'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Titre'),
        ),
        migrations.AlterField(
            model_name='article',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Vérifié'),
        ),
    ]
