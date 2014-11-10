from bulbs.contributions.models import Contribution

from collections import OrderedDict
from django.utils import timezone
from rest_framework import serializers

from .models import AccountingRule


class AccountingRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountingRule


class AccountingReportSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField("get_user")
    content = serializers.SerializerMethodField("get_content")
    role = serializers.SerializerMethodField("get_role")
    amount = serializers.SerializerMethodField("get_amount")

    class Meta:
        model = Contribution
        fields = ("id", "content", "user", "role", "amount")

    def get_amount(self, obj):
        rule = AccountingRule.objects.match(obj)
        if rule:
            return rule.amount
        return None

    def get_content(self, obj):
        return OrderedDict([
            ("id", obj.content.id),
            ("title", obj.content.title),
            ("url", obj.content.get_absolute_url()),
            ("content_type", obj.content.__class__.__name__),
            ("feature_type", obj.content.feature_type),
            ("published", timezone.localtime(obj.content.published))
        ])

    def get_user(self, obj):
        return {
            "id": obj.contributor.id,
            "username": obj.contributor.username,
            "full_name": obj.contributor.get_full_name(),
        }

    def get_role(self, obj):
        return obj.role.name
