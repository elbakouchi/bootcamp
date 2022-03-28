from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.translation import ugettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import F

from slugify import slugify

from django_comments.signals import comment_was_posted
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from bootcamp.custom import word_counter_validator
from bootcamp.notifications.models import Notification, notification_handler
from bootcamp.category.models import Category, Service


class DemandQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def get_category(self):
        return self.filter(verified=True).order_by('-updatedAt', '-createdAt').annotate(
            client_firstname=F('user__first_name'),
            client_lastname=F('user__last_name'),
            category_name=F('category__name'),
            category_slug=F('category__slug'),
            service_name=F('service__name'),
            revision_count=Count('revision__id', None)
        )

    def get_annotated_demand(self):
        return self.annotate(
            client_firstname=F('user__first_name'),
            client_lastname=F('user__last_name'),
            category_name=F('category__name'),
            category_slug=F('category__slug'),
            service_name=F('service__name'),
            revision_count=Count('revision__id', None)
        )

    def get_without_revisions(self):
        # return self.get_category().filter(has_revision=False)
        return self.filter(has_revision=False).order_by('-updatedAt', '-createdAt').annotate(
            client_firstname=F('user__first_name'),
            client_lastname=F('user__last_name'),
            category_name=F('category__name'),
            category_slug=F('category__slug'),
            service_name=F('service__name'),
            revision_count=Count('revision__id', None)
        )

    def get_revisions(self):
        return self.annotate(revisions=F('revision'))

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

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


class Demand(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    DEACTIVATED = "X"
    STATUS = ((DRAFT, _("Draft")), (PUBLISHED, _("Published")), (DEACTIVATED, _("Deactivated")))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="client",
        on_delete=models.SET_NULL,
    )

    service = models.ManyToManyField(
        Service,
        # null=True,
        related_name="demand_service"
        # on_delete=models.SET_NULL,
    )

    category = models.ManyToManyField(
        Category,
        # null=True,
        related_name="demand_category"
        # on_delete=models.SET_NULL,
    )
    '''
    image = models.ImageField(
        _("Featured image"), upload_to="demandes/%Y/%m/%d/", blank=True
    )
    '''
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = CKEditor5Field('Text', config_name='extends', validators=[word_counter_validator])
    verified = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    has_revision = models.BooleanField("Vérifié", default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = DemandQuerySet.as_manager()

    class Meta:
        verbose_name = _("Texte")
        verbose_name_plural = _("Textes")
        ordering = ("-timestamp",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.user.username}-{self.title}", lowercase=True, max_length=80
            )

        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)


def notify_comment(**kwargs):  # pragma: no cover
    """Handler to be fired up upon comments signal to notify the author of a
    given Demand."""
    actor = kwargs["request"].user
    receiver = kwargs["comment"].content_object.user
    obj = kwargs["comment"].content_object
    notification_handler(actor, receiver, Notification.COMMENTED, action_object=obj)


comment_was_posted.connect(receiver=notify_comment)
