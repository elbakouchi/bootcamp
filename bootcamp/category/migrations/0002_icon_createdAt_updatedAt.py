from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="icon",
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
         migrations.AddField(
            model_name="category",
            name="createdAt",
            field=models.DateTimeField(auto_now_add=True),
        ),
         migrations.AddField(
            model_name="category",
            name="updatedAt",
            field=models.DateTimeField(auto_now=True),
        )
        
    ]
