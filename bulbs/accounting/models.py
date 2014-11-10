from django.core.cache import cache
from django.db import models

from django.contrib.contenttypes.models import ContentType


import pickle


class AccountingRuleManager(models.Manager):

    def cached(self):
        cached = cache.get("accounting-rules")
        if cached is not None:
            return pickle.loads(cached)
        else:
            qs = self.all().prefetch_related("roles", "feature_types", "content_types")
            cache.set("accounting-rules", pickle.dumps(qs), 60 * 10)
            return qs

    def match(self, contribution):
        rules = self.cached()
        for rule in rules:
            if rule.match(contribution):
                return rule
        return None


class AccountingRule(models.Model):

    amount = models.FloatField()
    priority = models.IntegerField()

    roles = models.ManyToManyField("contributions.ContributorRole", null=True, blank=True)
    feature_types = models.ManyToManyField("content.FeatureType", null=True, blank=True)
    content_types = models.ManyToManyField("contenttypes.ContentType", null=True, blank=True)

    objects = AccountingRuleManager()

    def match(self, contribution):
        matched = False
        if self.roles.exists():
            if contribution.role_id not in self.roles.values_list("pk", flat=True):
                return False
            else:
                matched = True

        if self.feature_types.exists():
            if contribution.content.feature_type_id not in self.feature_types.values_list("pk", flat=True):
                return False
            else:
                matched = True

        if self.content_types.exists():
            content_type = ContentType.objects.get_for_model(contribution.content)
            if content_type.id not in self.content_types.values_list("pk", flat=True):
                return False
            else:
                matched = True

        return matched


class AccountingOverride(models.Model):
    amount = models.FloatField()
    contribution = models.ForeignKey("contributions.Contribution")
