from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from django.dispatch import Signal
from slugify import slugify
import spacy
from django.utils.html import strip_tags

from django_comments.signals import comment_was_posted
from markdownx.utils import markdownify
from taggit.managers import TaggableManager

from bootcamp.custom import word_counter_validator
from bootcamp.notifications.models import Notification, notification_handler, notification_checker
from bootcamp.category.models import Category, Service

from safedelete.managers import SafeDeleteManager, SafeDeleteAllManager
from safedelete.models import SafeDeleteModel, SOFT_DELETE

try:
    nlp = spacy.load("fr_core_news_sm")
except:
    spacy.cli.download("fr_core_news_sm")
    nlp = spacy.load("fr_core_news_sm")


class DemandQuerySet(models.query.QuerySet, SafeDeleteManager):
    """Personalized queryset created to improve model usability"""

    @staticmethod
    def get_last_revision():
        from bootcamp.articles.models import Article
        return models.Subquery(Article.objects.filter(
            demand_id=models.OuterRef("id"),
        ).order_by("-timestamp").values('content')[:1])

    def homepage(self):
        return self.filter(verified=True, deleted=None).distinct().annotate(
            categoryName=models.F('category__name'),
            category_slug=models.F('category__slug'),
            last_revision_content=self.get_last_revision(),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)).order_by("-timestamp")

    def profile(self, user_pk, order_by):
        if order_by == 'oldest':
            return self.filter(user=user_pk, deleted=None).order_by('pk', 'timestamp').annotate(
                service_name=models.F('service__name'),
                revision_count=models.Count('revision__id', None))
        elif order_by == 'newest':
            return self.filter(user=user_pk, deleted=None).order_by('-pk', '-timestamp').annotate(
                service_name=models.F('service__name'),
                revision_count=models.Count('revision__id', None))
        else:
            return self.filter(user=user_pk, deleted=None).order_by('pk', 'timestamp').annotate(
                service_name=models.F('service__name'),
                revision_count=models.Count('revision__id', None))

    def search(self, q):
        return self.filter(status="P", tokens__icontains=q, deleted=None).distinct().annotate(
            categoryName=models.F('category__name'),
            category_slug=models.F('category__slug'),
            last_revision_content=self.get_last_revision(),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)).order_by("-pk", "-timestamp")

    def get_category(self):
        return self.filter(verified=True, deleted=None).order_by('-updatedAt', '-createdAt').annotate(
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
            revision_count=models.Count('revision__id', None),
            last_revision_content=self.get_last_revision(),
        )

    def get_category_demands(self, category):
        print(category)
        return self.filter(status="P", deleted=None, category__slug=category).distinct().order_by(
            '-timestamp').annotate(
            client_firstname=models.F('user__first_name'),
            client_lastname=models.F('user__last_name'),
            category_name=models.F('category__name'),
            category_slug=models.F('category__slug'),
            last_revision_content=self.get_last_revision(),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)
        )  # .filter(category_slug=category)

    def get_published_unverified_demands(self, limit=None):
        qs = self.filter(status="P", deleted=None, verified=False).distinct().order_by('-timestamp').annotate(
            client_firstname=models.F('user__first_name'),
            client_lastname=models.F('user__last_name'),
            category_name=models.F('category__name'),
            category_slug=models.F('category__slug'),
            last_revision_content=self.get_last_revision(),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)
        )  # .filter(revision_count=0)
        if limit:
            return qs[:limit]
        return qs

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

    # def search_tokens(self, token):
    #    return self.filter(status="P").annotate(tokens=[yield token for token in self.tokens])

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

    def corrected_demands(self):
        return self.filter(verified=True, deleted=None).distinct().annotate(
            categoryName=models.F('category__name'),
            category_slug=models.F('category__slug'),
            last_revision_content=self.get_last_revision(),
            service_name=models.F('service__name'),
            revision_count=models.Count('revision__id', None)).order_by("-timestamp")


class Demand(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
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
    objectz = DemandQuerySet.as_manager()
    objects = SafeDeleteAllManager()
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
        self.slug = slugify(
            f"{self.title}-{self.user.pk}", lowercase=True, max_length=80
        )
        if not self.slug:
            pass
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
        if self.status == self.PUBLISHED:
            demand_is_published.send(sender=self.__class__, demand=self.demand)
            if self.verified:
                demand_is_validated.send(sender=self.__class__, demand=self.demand)

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


def broadcast_demand_validated(sender, user, request, **kwargs):
    demand = kwargs["demand"]
    exists = notification_checker(user, demand.user, Notification.DEMAND_VALIDATED, action_object=demand)
    if not exists:
        notification_handler(user, demand.user, Notification.DEMAND_VALIDATED, action_object=demand)


def broadcast_demand_published(sender, user, request, **kwargs):
    demand = kwargs["demand"]
    exists = notification_checker(user, demand.user, Notification.DEMAND_PUBLISHED, action_object=demand)
    if not exists:
        notification_handler(user, demand.user, Notification.DEMAND_PUBLISHED, action_object=demand)


demand_is_published = demand_is_validated = Signal()
demand_is_published.connect(broadcast_demand_published)
demand_is_validated.connect(broadcast_demand_validated)
comment_was_posted.connect(receiver=notify_comment)
