import datetime
from elastimorphic.tests.base import BaseIndexableTestCase

from bulbs.content.models import FeatureType
from bulbs.contributions.models import ContributorRole, Contribution
from bulbs.accounting.models import AccountingRule

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
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

    def test_simple_matching(self):
        client = Client()
        client.login(username="admin", password="secret")

        rule = AccountingRule.objects.create(
            amount=100.00,
            priority=0
        )
        rule.roles.add(self.roles["editor"])

        content = make_content(published=timezone.now() - datetime.timedelta(hours=2))

        Contribution.objects.create(
            contributor=self.authors[0],
            content=content,
            role=self.roles["editor"]
        )
        Contribution.objects.create(
            contributor=self.authors[0],
            content=content,
            role=self.roles["writer"]
        )

        # Let's look at all the items
        endpoint = reverse("accountingreport-list")
        start_date = timezone.now() - datetime.timedelta(days=4)
        response = client.get(endpoint, data={"start": start_date.strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
