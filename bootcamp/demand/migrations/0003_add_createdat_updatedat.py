from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("demand", "0001_initial"),
        ("demand", "0002_alter_image_null"),
    ]

    operations = [

        migrations.AddField(
            model_name="demand",
            name="createdAt",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name="demand",
            name="updatedAt",
            field=models.DateTimeField(auto_now=True),
        )

    ]
