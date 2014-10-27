"""API Views and ViewSets"""

from rest_framework import viewsets, routers

from bulbs.api.permissions import IsAdminUser
from bulbs.api.mixins import UncachedResponse

from .models import AccountingRule
from .serializers import AccountingRuleSerializer


class AccountingRuleViewSet(UncachedResponse, viewsets.ModelViewSet):
    model = AccountingRule
    serializer_class = AccountingRuleSerializer

    permission_classes = [IsAdminUser]


api_v1_router = routers.DefaultRouter()
api_v1_router.register(r"rule", AccountingRuleViewSet, base_name="rule")
