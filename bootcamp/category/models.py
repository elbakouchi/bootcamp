from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _

from slugify import slugify

# from django_comments.signals import comment_was_posted
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from bootcamp.notifications.models import Notification, notification_handler


class CategoryQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""
    def get_demands(self):
        return self.annotate(articles='demand_category__demand')

    def get_articles(self):
        self.filter(activated=True).annotate(taxonomy_category__article=())

    def get_activated(self):
        """Returns only the activated items in the current queryset."""
        return self.filter(activated=True)

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    def get_counted_tags(self):
        tag_dict = {}
        query = (
            self.filter(status="P").annotate(tagged=Count("tags")).filter(tags__gt=0)
        )
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()

    @staticmethod
    def get_categories_with_demands_count():
        return Category.objects.filter(activated=True).annotate(posts_count=Count('demand_category'))

    # @staticmethod
    def get_categories_with_articles(self):
        # articles = Article.objects.get_by_demand()
        return self.filter(activated=True)


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="createdBy",
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(
        _("Featured image"), upload_to="categories/%Y/%m/%d/", blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    description = models.TextField(max_length=280)
    activated = models.BooleanField(default=False)
    tags = TaggableManager()
    icon = models.CharField(max_length=255, null=True, blank=True)
    objects = CategoryQuerySet.as_manager()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.name}-{self.pk}", lowercase=True, max_length=80
            )

        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.description)


# def notify_comment(**kwargs):  # pragma: no cover
#     """Handler to be fired up upon comments signal to notify the author of a
#     given Category."""
#     actor = kwargs["request"].user
#     receiver = kwargs["comment"].description_object.user
#     obj = kwargs["comment"].description_object
#     notification_handler(actor, receiver, Notification.COMMENTED, action_object=obj)


# comment_was_posted.connect(receiver=notify_comment)

class ServiceQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_activated(self):
        """Returns only the published items in the current queryset."""
        return self.filter(activated=True)

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    def get_counted_tags(self):
        tag_dict = {}
        query = (
            self.filter(status="P").annotate(tagged=Count("tags")).filter(tags__gt=0)
        )
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()


class Service(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="addedBy",
        on_delete=models.SET_NULL,
    )
    image = models.ImageField(
        _("Featured image"), upload_to="services/%Y/%m/%d/", blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    description = models.TextField(max_length=280)
    activated = models.BooleanField(default=False)
    tags = TaggableManager()
    icon = models.CharField(max_length=255, null=True, blank=True)
    objects = ServiceQuerySet.as_manager()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.name}", lowercase=True, max_length=80
            )

        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.description)
