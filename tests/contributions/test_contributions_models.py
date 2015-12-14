from django.contrib.auth import get_user_model
from django.utils import timezone

from freezegun import freeze_time

from bulbs.content.models import *
from bulbs.contributions.models import Contribution, ContributorRole, FeatureTypeRate
from bulbs.utils.test import BaseIndexableTestCase


User = get_user_model()


class ContributionModelTestCase(BaseIndexableTestCase):

    def setUp(self):
        super(ContributionModelTestCase, self).setUp()
        self.freezer = freeze_time("2015-09-25")
        self.freezer.start()
        self.feature_types = {
            'tv-club': FeatureType.objects.create(name='T.V. Club', slug='tv-club')
        }
        self.roles = {
            'big-dog': ContributorRole.objects.create(name='Big Dog', payment_type=1)
        }
        self.contributors = {
            'cammy': User.objects.create(
                username='clowe', is_staff=True, first_name='cameron', last_name='lowe'
            )
        }
        self.content = [
            Content.objects.create(
                feature_type=self.feature_types['tv-club'],
                published=timezone.datetime(year=2015, month=9, day=21)
            )
        ]

    def tearDown(self):
        self.freezer.stop()
        super(ContributionModelTestCase, self).tearDown()

    def test_elasticsearch(self):
        # Test elasticsearch pay
        ft_rate = FeatureTypeRate.objects.get(
            role=self.roles['big-dog'],
            feature_type=self.feature_types['tv-club']
        )
        ft_rate.rate = 200
        ft_rate.save()
        Contribution.objects.create(
            role=self.roles['big-dog'],
            contributor=self.contributors['cammy'],
            content=self.content[0]
        )
        Contribution.search_objects.refresh()
        elastic_queryset = Contribution.search_objects.search()
        self.assertEqual(elastic_queryset.count(), 1)
        ec = elastic_queryset[0]
        self.assertEqual(ec.pay, 200)
