from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from slugify import slugify
import spacy
from django.utils.html import strip_tags

from django_comments.signals import comment_was_posted
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from bootcamp.custom import word_counter_validator
from bootcamp.notifications.models import Notification, notification_handler
from bootcamp.category.models import Category, Service

try:
    nlp = spacy.load("fr_core_news_sm")
except:
    spacy.cli.download("fr_core_news_sm")
    nlp = spacy.load("fr_core_news_sm")


class DemandQuerySet(models.query.QuerySet):
    """Personalized queryset created to improve model usability"""

    def homepage(self):
        from bootcamp.articles.models import Article
        latest_revision = models.Subquery(Article.objects.filter(
            demand_id=models.OuterRef("id"),
        ).order_by("-timestamp").values('content')[:1])
        return self.filter(verified=True).distinct().annotate(
            categoryName=models.F('category__name'),
            last_revision_content=latest_revision,
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)).order_by("-pk", "-timestamp")

    def get_category(self):
        return self.filter(verified=True).order_by('-updatedAt', '-createdAt').annotate(
            client_firstname=models.F('user__first_name'),
            client_lastname=models.F('user__last_name'),
            category_name=models.F('category__name'),
            category_slug=models.F('category__slug'),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)
        )

    def get_annotated_demand(self):
        return self.annotate(
            client_firstname=models.F('user__first_name'),
            client_lastname=models.F('user__last_name'),
            category_name=models.F('category__name'),
            category_slug=models.F('category__slug'),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)
        )

    def get_published_unverified_demands(self):
        return self.filter(status="P", verified=False).distinct().order_by('-updatedAt', '-createdAt').annotate(
            client_firstname=models.F('user__first_name'),
            client_lastname=models.F('user__last_name'),
            category_name=models.F('category__name'),
            category_slug=models.F('category__slug'),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)
        )

    def get_without_revisions(self):
        # return self.get_category().filter(has_revision=False)
        return self.filter(has_revision=False).order_by('-updatedAt', '-createdAt').annotate(
            client_firstname=models.F('user__first_name'),
            client_lastname=models.F('user__last_name'),
            category_name=models.F('category__name'),
            category_slug=models.F('category__slug'),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)
        )

    def get_revisions(self):
        return self.annotate(revisions=models.F('revision'))

    def get_published(self):
        """Returns only the published items in the current queryset."""
        return self.filter(status="P")

    def get_drafts(self):
        """Returns only the items marked as DRAFT in the current queryset."""
        return self.filter(status="D")

    def get_counted_tags(self):
        tag_dict = {}
        query = (
            self.filter(status="P").annotate(tagged=models.Count("tags")).filter(tags__gt=0)
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
    verified = models.BooleanField("Vérifié", default=False)
    tags = TaggableManager(blank=True)
    has_revision = models.BooleanField("N'est pas en attente", default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    objects = DemandQuerySet.as_manager()
    keywords = models.TextField(blank=True, verbose_name="Mots clés SEO", help_text="nécessaire à la SEO")
    tokens = models.TextField(blank=True, verbose_name="Mots clés Recherche",
                              help_text="nécessaire pour la recherche texte")

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
        doc = nlp(strip_tags(self.content))
        if not self.tokens:
            tags = [token.lemma_ for token in doc if token.pos_ in ["VERB", "ADVERB", "NOUN"]]
            chunks = [chunk.text for chunk in doc.noun_chunks]
            self.tokens = ",".join(tags + chunks)
        if not self.keywords:
            # doc = nlp(strip_tags(self.content))
            tags = [token.lemma_ for token in doc if token.pos_ in ["NOUN"]]
            try:
                self.keywords = f"{self.tags},{','.join(tags)}"
            except:
                self.keywords = ','.join(tags)
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
