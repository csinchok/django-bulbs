from django.core.cache import cache
from django.db import models

from bulbs.contributions.models import ContributorRole, Contribution
from bulbs.content.models import FeatureType
from django.contrib.contenttypes.models import ContentType


class AccountingRuleManager(models.Manager):

    def cached(self):
        rules = cache.get("accounting-rules")
        if rules is None:
            rules = self.objects.values()
            cache.set("accounting-rules", rules, 60 * 10)
        return [AccountingRule(**rule) for rule in rules]

    def match(self, contribution):
        rules = self.cached()
        for rule in rules:
            if rule.roles:
                if contribution.role_id not in rule.roles:
                    return False
            if rule.feature_types:
                if contribution.content.feature_type_id not in rule.feature_types:
                    return False
            if rule.content_types:
                content_type = ContentType.objects.get_for_model(contribution.content)
                if content_type.id not in rule.content_types:
                    return False
        return True


class AccountingRule(models.Model):

    amount = models.FloatField()
    priority = models.IntegerField()

    roles = models.ManyToMany(ContributorRole, null=True, blank=True)
    feature_types = models.ManyToMany(FeatureType, null=True, blank=True)
    content_types = models.ManyToMany(ContentType, null=True, blank=True)


class AccountingOverride(models.Model):
    amount = models.FloatField()
    contribution = models.ForeignKey(Contribution)
