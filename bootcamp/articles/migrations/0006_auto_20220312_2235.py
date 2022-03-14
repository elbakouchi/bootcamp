# Generated by Django 3.2.12 on 2022-03-12 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demand', '0008_auto_20220305_1612'),
        ('articles', '0005_auto_20220305_1137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Révision', 'verbose_name_plural': 'Révisions'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='article',
            name='demand',
        ),
        migrations.AddField(
            model_name='article',
            name='demand',
            field=models.ManyToManyField(null=True, related_name='demand', to='demand.Demand'),
        ),
    ]
