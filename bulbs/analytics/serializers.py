from django.template.loader import render_to_string
from rest_framework import serializers

from .models import SocialPromotion


class SocialPromotionSerializer(serializers.ModelSerializer):

    rendered = serializers.SerialierMethodField()

    class Meta:
        model = SocialPromotion

    def get_rendered(self, obj):
        return render_to_string("analytics/social/{}.html".format(obj.__class__.__name__.lower()))
