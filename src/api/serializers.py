from rest_framework import serializers

from .models import Donation
from .models import Ambassador
from .models import TeamMember
from .models import Partner
from .models import GreenChampion
from .models import YouTubeLink
from .models import FAQ
from .models import LearnMore
from .models import USDRate
from .models import PaySysTransaction
from .models import ClassyTransaction
from .models import NewsModel

class PaySysTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaySysTransaction
        fields = '__all__'


class ClassyTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassyTransaction
        fields = '__all__'


class DonationListSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')
    amount = serializers.SerializerMethodField('get_amount')

    def get_display_name(self, obj):
        if obj.is_anonymous:
            return 'Anonymous'
        return obj.display_name

    def get_amount(self, obj):
        if obj.payment_currency == Donation.PaymentCurrency.UZS:
            usd = USDRate.objects.latest('created')
            return ('%0.2f' % (obj.amount/usd.rate)).replace('.00', '')
        return obj.amount

    class Meta:
        model = Donation
        fields = [
            'created',
            'amount',
            'display_name',
            'message',
            'is_gift',
        ]
        read_only_fields = ['amount', 'display_name', 'message', 'is_gift']


class AmbassadorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambassador
        fields = [
            'name',
            'description',
            'avatar',
        ]
        read_only_fields = [
            'name',
            'description',
            'avatar',
            'created',
            'creator',
            'is_published',
        ]


class TeamMemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            'name',
            'description',
            'avatar',
        ]
        read_only_fields = [
            'name',
            'description',
            'avatar',
            'created',
            'creator',
            'is_published',
        ]


class PartnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = [
            'name',
            'link',
            'is_link_enabled',
            'logo',
        ]
        read_only_fields = [
            'name',
            'link',
            'is_link_enabled',
            'logo',
            'created',
            'creator',
            'is_published',
        ]


class GreenChampionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreenChampion
        fields = [
            'name',
            'link',
            'is_link_enabled',
            'logo',
        ]
        read_only_fields = [
            'name',
            'link',
            'is_link_enabled',
            'logo',
            'created',
            'creator',
            'is_published',
        ]


class YouTubeLinkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeLink
        fields = [
            'description',
            'link',
            'snapshot',
        ]
        read_only_fields = [
            'description',
            'link',
            'snapshot',
            'created',
            'creator',
            'is_published',
        ]


class LearnMoreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnMore
        fields = [
            'title',
            'description',
            'link',
            'background_image',
        ]
        read_only_fields = [
            'title',
            'description',
            'link',
            'background_image',
            'is_published',
            'created',
            'creator',
        ]


class FAQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = [
            'question',
            'answer',
        ]
        read_only_fields = [
            'description',
            'link',
            'created',
            'creator',
            'is_published',
        ]


class USDRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = USDRate
        fields = [
            'rate',
        ]
        read_only_fields = [
            'rate',
            'created',
            'creator',
        ]


class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = [
            'id',  # 'id' is added to the fields list
            'title',
            'description',
            'image',
            'created',
            ]
        read_only_fields = [
            'created',
        ]