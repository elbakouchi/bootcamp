# Generated by Django 3.2.12 on 2022-03-20 13:46

import django.core.validators
from django.db import migrations, models
import django_ckeditor_5.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('demand', '0008_auto_20220305_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='has_revision',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='demand',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(validators=[django.core.validators.MaxLengthValidator(100)], verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
