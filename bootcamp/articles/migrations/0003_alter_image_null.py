import django.contrib.sites.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('articles', '0001_initial'), ('articles', '0002_auto_20220219_1042'), ("demand", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="image",
            field=models.ImageField(
                        upload_to="articles/%Y/%m/%d/",
                        verbose_name="Featured image",
                        null=True
                    ),
        )

        
    ]
