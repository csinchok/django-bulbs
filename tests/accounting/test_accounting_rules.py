from elastimorphic.tests.base import BaseIndexableTestCase

from bulbs.content.models import FeatureType
from bulbs.contributions.models import ContributorRole, Contribution
from bulbs.accounting.models import AccountingRule

from django.contrib.auth.models import User
from django.utils import timezone


from tests.utils import make_content
from model_mommy import mommy


class TestAccountingRules(BaseIndexableTestCase):

    def setUp(self):
        super(TestAccountingRules, self).setUp()

        self.feature_types = {}
        for name in ("clicks", "clacks", "clunks"):
            self.feature_types[name] = mommy.make(FeatureType, name=name)

        self.roles = {}
        for name in ("editor", "writer", "contributor"):
            self.roles[name] = mommy.make(ContributorRole, name=name)

        self.authors = mommy.make(User, _quantity=20)

    def test_cached_rules(self):
        rule = AccountingRule.objects.create(
            amount=100.00,
            priority=0
        )
        rule.roles.add(self.roles["editor"])

        rules = AccountingRule.objects.cached()
        self.assertEqual(rules[0].roles.count(), 1)

    def test_simple_matching(self):
        rule = AccountingRule.objects.create(
            amount=100.00,
            priority=0
        )
        rule.roles.add(self.roles["editor"])

        content = make_content(published=timezone.now())
        contribution = Contribution.objects.create(
            contributor=self.authors[0],
            content=content,
            role=self.roles["editor"]
        )
        self.assertTrue(rule.match(contribution))
        self.assertEqual(AccountingRule.objects.match(contribution), rule)

        orphaned_contribution = Contribution.objects.create(
            contributor=self.authors[0],
            content=content,
            role=self.roles["writer"]
        )
        self.assertFalse(rule.match(orphaned_contribution))
        self.assertIsNone(AccountingRule.objects.match(orphaned_contribution))
