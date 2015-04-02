from django_filters import DateTimeFilter, FilterSet
from rest_framework import routers, viewsets, filters

from .models import Campaign
from .serializers import CampaignSerializer


class CampaignFilter(FilterSet):
    start_date = DateTimeFilter(lookup_type="lte")
    end_date = DateTimeFilter(lookup_type="gt")

    class Meta:
        model = Campaign
        fields = ["start_date", "end_date"]


class CampaignViewSet(viewsets.ModelViewSet):
    model = Campaign
    serializer_class = CampaignSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    filter_class = CampaignFilter
    paginate_by = 10
    search_fields = ("campaign_label", "sponsor_name")
    ordering_fields = ("campaign_label", "sponsor_name", "start_date", "end_date")

api_v1_router = routers.DefaultRouter()
api_v1_router.register(
    r"campaign",
    CampaignViewSet,
    base_name="campaign")
