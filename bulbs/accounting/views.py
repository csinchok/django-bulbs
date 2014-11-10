"""API Views and ViewSets"""

import datetime

from django.utils import timezone, dateparse

from rest_framework import viewsets, routers
from rest_framework.settings import api_settings
from rest_framework_csv.renderers import CSVRenderer

from bulbs.api.mixins import UncachedResponse
from bulbs.content.models import Content
from bulbs.contributions.models import Contribution

from .models import AccountingRule, AccountingOverride
from .serializers import AccountingRuleSerializer, AccountingReportSerializer


class AccountingRuleViewSet(UncachedResponse, viewsets.ModelViewSet):
    model = AccountingRule
    serializer_class = AccountingRuleSerializer

    # permission_classes = [IsAdminUser]


class AccountingReportViewSet(UncachedResponse, viewsets.ModelViewSet):

    renderer_classes = (CSVRenderer, ) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    serializer_class = AccountingReportSerializer

    def get_queryset(self):
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
        contributions = Contribution.objects.filter(content__in=content_ids)

        ordering = self.request.GET.get("ordering", "content")
        order_options = {
            "content": "content__published",
            "user": "contributor__id"
        }
        return contributions.order_by(order_options[ordering])


api_v1_router = routers.DefaultRouter()
api_v1_router.register(r"rule", AccountingRuleViewSet, base_name="rule")
api_v1_router.register(r"accountingreport", AccountingReportViewSet, base_name="accountingreport")
