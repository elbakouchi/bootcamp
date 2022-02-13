# Generated by Django 2.0.3 on 2018-07-04 03:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markdownx.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True
    '''
    dependencies = [
        ("taggit", "0002_auto_20150616_2121"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]'''
    operations = [
        migrations.CreateModel(
            name="Categoy",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="articles_pictures/%Y/%m/%d/",
                        verbose_name="Featured image",
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(blank=True, max_length=80, null=True)),
                
                ("description", markdownx.models.MarkdownxField()),
                ("activated", models.BooleanField(default=False)),
                ("icon", models.)
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="author",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Categoy",
                "verbose_name_plural": "Categoies",
                "ordering": ("-timestamp",),
            },
        )
    ]
