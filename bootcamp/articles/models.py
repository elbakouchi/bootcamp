from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.dispatch import Signal
from django.utils.translation import ugettext_lazy as _

from django_ckeditor_5.fields import CKEditor5Field
from django.db.models import F
from slugify import slugify
from django.utils.html import format_html

import bootcamp.demand.models
from django_comments.signals import comment_was_posted
from markdownx.utils import markdownify

from bootcamp.custom import word_counter_validator
from bootcamp.notifications.models import Notification, notification_handler
from bootcamp.users.models import User

import os

from safedelete.models import SafeDeleteModel, SOFT_DELETE


class ArticleAuthor(User):
    class Meta:
        proxy = True
        verbose_name = _("Auteur")
        verbose_name_plural = _("Auteurs")
        

class ArticleQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    # def get_page_views(self):
    #    path = reverse('articles:article', args=[self.slug])
    #    count = Pageview.objects.filter()
    #    return self.annotate(page_views=)
    def get_category(self):
        return self.annotate(
            category_name=F('demand__category__name'),
            category_slug=F('demand__category__slug'))

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    def get_by_demand(self, category):
        return self.filter()


class Article(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = ((DRAFT, _("Draft")), (PUBLISHED, _("Published")))

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="author",
        on_delete=models.SET_NULL,
    )

    demand = models.ForeignKey(
        bootcamp.demand.models.Demand,
        null=True,
        related_name="revision",
        on_delete=models.SET_NULL
    )
    '''
    image = models.ImageField(
        _("Featured image"), upload_to="articles/%Y/%m/%d/", blank=True
    )
    '''
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField("Titre", max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField("État", max_length=1, choices=STATUS, default=DRAFT)
    content = CKEditor5Field('Contenu', config_name='extends', validators=[word_counter_validator])
    verified = models.BooleanField("Vérifié", default=False)
    # tags = TaggableManager()
    objects = ArticleQuerySet.as_manager()

    # @staticmethod

    # def __init__(self, *args, **kwargs):
    #    super(Article, self).__init__()
    #    self.objects.get_category

    class Meta:
        verbose_name = _("Révision")
        verbose_name_plural = _("Révisions")
        ordering = ("-timestamp",)

    def __str__(self):
        # self.get_category()
        return f"{self.title}"  # -{self.}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.title}-{self.id}", lowercase=True, max_length=80
            )

        super().save(*args, **kwargs)
        if self.verified and os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
            demand_has_revision.send(sender=self,
                                     demand=self.demand
                                    )
            try:                        
                revision_created.send(sender=self.__class__,
                                     demand=self.demand
                                    )                        
            except:
                pass
            
    def get_markdown(self):
        return markdownify(self.content)


def notify_comment(**kwargs):  # pragma: no cover
    """Handler to be fired up upon comments signal to notify the author of a
    given article."""
    actor = kwargs["request"].user
    receiver = kwargs["comment"].content_object.user
    obj = kwargs["comment"].content_object
    notification_handler(actor, receiver, Notification.COMMENTED, action_object=obj)


def set_demand_has_revision(**kwargs):
    demand = kwargs["demand"]
    revision = kwargs['sender']
    print(revision.content)
    if not demand.has_revision:
        demand.has_revision = True
    demand.update_when_revisioned(revision.content)
    demand.save()
    print(kwargs["demand"], "has revision")


def broadcast_revision_created(sender, user, request, **kwargs):
    try:
        demand = kwargs["demand"]
        notification_handler(user, demand.user, Notification.REVISION_ADDED, action_object=demand)
    except TypeError as e:
        pass


if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
  demand_has_revision = Signal()
  revision_created = Signal()
  demand_has_revision.connect(receiver=set_demand_has_revision)
  try:
   revision_created.connect(receiver=broadcast_revision_created)
  except Exception as e:
    print(e) 
  comment_was_posted.connect(receiver=notify_comment)
