import django.contrib.sites.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("demand", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="demand",
            name="image",
            field=models.ImageField(
                        upload_to="articles_pictures/%Y/%m/%d/",
                        verbose_name="Featured image",
                        null=True
                    ),
        )
    ]
