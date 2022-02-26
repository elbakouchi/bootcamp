# Generated by Django 3.2.10 on 2022-02-19 10:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
       # ('category', '0003_auto_20220219_1042'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demand', '0003_add_createdat_updatedat'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='demand',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Demand', 'verbose_name_plural': 'Demands'},
        ),
        migrations.AlterField(
            model_name='demand',
            name='category',
            field=models.ManyToManyField(null=True, related_name='taxonomy_category', to='category.Category'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='demandes/%Y/%m/%d/', verbose_name='Featured image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='demand',
            name='service',
            field=models.ManyToManyField(null=True, related_name='taxonomy_service', to='category.Service'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
