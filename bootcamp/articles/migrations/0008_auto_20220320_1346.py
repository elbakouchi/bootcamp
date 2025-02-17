# Generated by Django 3.2.12 on 2022-03-20 13:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0008_auto_20220305_1612'),
        ('articles', '0007_auto_20220315_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(validators=[django.core.validators.MaxLengthValidator(100)], verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='article',
            name='demand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='revision', to='demand.demand'),
        ),
    ]
