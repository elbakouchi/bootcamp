# Generated by Django 3.2.12 on 2022-04-29 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0013_demand_tokens'),
    ]

    operations = [
        migrations.AddField(
            model_name='demand',
            name='keywords',
            field=models.TextField(blank=True, help_text='nécessaire à la SEO', verbose_name='Mots clés SEO'),
        ),
        migrations.AlterField(
            model_name='demand',
            name='tokens',
            field=models.TextField(blank=True, help_text='nécessaire pour la recherche texte', verbose_name='Mots clés Recherche'),
        ),
    ]
