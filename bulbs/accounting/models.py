from django.db import models

from bulbs.contributions.models import ContributorRole, Contribution
from bulbs.content.models import FeatureType
from django.contrib.contenttypes.models import ContentType


class AccountingRule(models.Model):

    amount = models.FloatField()
    priority = models.IntegerField()

    roles = models.ManyToMany(ContributorRole, null=True, blank=True)
    feature_types = models.ManyToMany(FeatureType, null=True, blank=True)
    content_types = models.ManyToMany(ContentType, null=True, blank=True)


class AccountingOverride(models.Model):
    amount = models.FloatField()
    contribution = models.ForeignKey(Contribution)
