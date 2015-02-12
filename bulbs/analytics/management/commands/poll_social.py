import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from bulbs.analytics.models import SocialAccount, SocialPromotion


class Command(BaseCommand):
    help = 'Polls social accounts for new posts, and their analytics'

    def handle(self, *args, **options):
        for account in SocialAccount.objects.all():
            account.poll()

        now = timezone.now()
        two_days_ago = now - datetime.timedelta(days=1)
        one_week_ago = now - datetime.timedelta(days=7)
        polling_rules = [
            {
                "created_time__gte": two_days_ago,
                "last_updated__lte": datetime.timedelta(minutes=15)
            },
            {
                "created_time__range": (one_week_ago, two_days_ago),
                "last_updated__lte": datetime.timedelta(hours=1)
            },
        ]

        for kwargs in polling_rules:
            for promotion in SocialPromotion.objects.filter(**kwargs):
                promotion.update_analytics()
