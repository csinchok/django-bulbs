"""API Views and ViewSets"""

import datetime

from django.utils import timezone, dateparse

from rest_framework import viewsets, routers

from bulbs.api.permissions import IsAdminUser
from bulbs.api.mixins import UncachedResponse
from bulbs.content.models import Content

from .models import AccountingRule, AccountingOverride
from .serializers import AccountingRuleSerializer


class AccountingRuleViewSet(UncachedResponse, viewsets.ModelViewSet):
    model = AccountingRule
    serializer_class = AccountingRuleSerializer

    permission_classes = [IsAdminUser]


class AccountingReportViewSet(UncachedResponse, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        now = timezone.now()

        start_date = datetime.datetime(
            year=now.year,
            month=now.month,
            day=1,
            tzinfo=now.tzinfo)
        if "start" in self.request.GET:
            start_date = dateparse.parse_date(self.request.GET["start"])

        end_date = now
        if "end" in self.request.GET:
            end_date = dateparse.parse_date(self.request.GET["end"])

        content = Content.objects.filter(published__range=(start_date, end_date))
        content_ids = content.values_list("pk", flat=True)

        rules = AccountingRule.objects.all()
        contributions = Contribution.objects.filter(content__in=content_ids).select_related("content")
        contribution_ids = contributions.values_list("pk", flat=True)
        overrides = AccountingOverride.objects.filter(contribution__in=contribution_ids)

        data = []
        for contribution in contributions:
            for rule in rules:
                if rule.matches(content)
            data.append({
                "author": contribution.contributor,
                "content": contribution.content,
                "amount": 
            })


api_v1_router = routers.DefaultRouter()
api_v1_router.register(r"rule", AccountingRuleViewSet, base_name="rule")
