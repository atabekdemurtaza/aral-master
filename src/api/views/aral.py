from hashlib import md5
from datetime import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Case, When, F, FloatField
from rest_framework.response import Response
from django.http import HttpResponseRedirect


from rest_framework import status
from rest_framework import views
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.models import Donation
from api.models import Ambassador
from api.models import TeamMember
from api.models import Partner
from api.models import GreenChampion
from api.models import LearnMore
from api.models import YouTubeLink
from api.models import FAQ
from api.models import USDRate
from api.models import NewsModel

from api.serializers import DonationListSerializer
from api.serializers import AmbassadorListSerializer
from api.serializers import TeamMemberListSerializer
from api.serializers import PartnerListSerializer
from api.serializers import GreenChampionListSerializer
from api.serializers import LearnMoreListSerializer
from api.serializers import YouTubeLinkListSerializer
from api.serializers import FAQListSerializer
from api.serializers import NewsModelSerializer


class TotalDonationAmountView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        usd_rate = USDRate.objects.latest('created')

        total_uzb = Donation.objects.total_uzs_amount()
        total_usd = Donation.objects.total_usd_amount()

        uzb = total_uzb.get('amount__sum') or 0
        usd = total_usd.get('amount__sum') or 0

        total = round(uzb/usd_rate.rate) + usd
        return Response(
            {
                "total_donations": {
                    'amount__sum': total,
                },
            }
        )


class DonationPagination(PageNumberPagination):
    page_size = settings.NUMBER_OF_DONATIONS_TO_SHOW
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MostRecentDonationListView(generics.ListAPIView):
    serializer_class = DonationListSerializer
    pagination_class = DonationPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ('-created',)
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Donation.objects.all()

class MostAmountDonationListView(generics.ListAPIView):
    serializer_class = DonationListSerializer
    pagination_class = DonationPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ('-calculated_amount', 'created')
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Donation.objects.annotate(
            calculated_amount=Case(
                When(
                    payment_currency=Donation.PaymentCurrency.UZS,
                    then=F('amount')/10000.0,
                ),
                default=F('amount'),
                output_field=FloatField(),
            )
        )


class AmbassadorListView(generics.ListAPIView):
    serializer_class = AmbassadorListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Ambassador.objects.filter(is_published=True)


class TeamMemberListView(generics.ListAPIView):
    serializer_class = TeamMemberListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return TeamMember.objects.filter(is_published=True)


class PartnerListView(generics.ListAPIView):
    serializer_class = PartnerListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Partner.objects.filter(is_published=True)


class GreenChampionListView(generics.ListAPIView):
    serializer_class = GreenChampionListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return GreenChampion.objects.filter(is_published=True)


class LearnMoreListView(generics.ListAPIView):
    serializer_class = LearnMoreListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return LearnMore.objects.filter(is_published=True)


class YouTubeLinkListView(generics.ListAPIView):
    serializer_class = YouTubeLinkListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return YouTubeLink.objects.filter(is_published=True)


class FAQListView(generics.ListAPIView):
    serializer_class = FAQListSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return FAQ.objects.filter(is_published=True)


class NewsModelListView(generics.ListAPIView):
    serializer_class = NewsModelSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return NewsModel.objects.filter(is_published=True).order_by('-created')

class NewsDetailView(generics.RetrieveAPIView):
    queryset = NewsModel.objects.all()
    serializer_class = NewsModelSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        obj_id = self.kwargs.get('pk')  # or 'id' if your URL pattern uses <int:id>
        return get_object_or_404(NewsModel, pk=obj_id)


class RedirectView(views.APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        agr_uz_pay_url = "https://agr.uz/pay"        
        # You can handle the payload and response here if needed
        
        # Redirect to the desired URL
        return HttpResponseRedirect(agr_uz_pay_url)