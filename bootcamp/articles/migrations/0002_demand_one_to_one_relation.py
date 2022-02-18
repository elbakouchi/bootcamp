import django.contrib.sites.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("articles", "0001_initial")]

    operations = [
        migrations.AddField
        (
            "demand",
            models.OneToOneField(
                blank=True,
                help_text="Demand explaining this article category and service.",
                related_query_name="demand",
                verbose_name="Demand",
                related_name="demand",
                on_delete=models.SET_NULL,
                to="demand.Demand",
            ),
        )
    ]
