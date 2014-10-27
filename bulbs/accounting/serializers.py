from rest_framework import serializers

from .models import AccountingRule


class AccountingRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountingRule

