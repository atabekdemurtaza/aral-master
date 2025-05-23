from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet
from django.db.models import Sum
from django.conf import settings

from .validators import ImageDimensionsValidator


class DonationQuerySet(QuerySet):
    def total_uzs_amount(self):
        """ Calculate total amount of donations """
        return self.filter(
            payment_currency=Donation.PaymentCurrency.UZS,
        ).aggregate(
            Sum('amount'),
        )

    def total_usd_amount(self):
        """ Calculate total amount of donations """
        return self.filter(
            payment_currency=Donation.PaymentCurrency.USD,
        ).aggregate(
            Sum('amount'),
        )


class DonationManager(models.Manager):
    def get_query_set(self):
        return DonationQuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith('_'):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)


class PaySysTransaction(models.Model):
    class PaymentStatus(models.IntegerChoices):
        INITIATED = 1, _('INITIATED')
        PAYED = 2, _('PAYED')
        CANCELED = 3, _('CANCELED')

    class PaymentEnvironment(models.IntegerChoices):
        LIVE = 1, _('LIVE')
        SANDBOX = 2, _('SANDBOX')

    payment_environment = models.IntegerField(
        _('EVIRONMENT'),
        choices=PaymentEnvironment.choices,
        blank=False,
        default=PaymentEnvironment.LIVE,
    )
    payment_agr_trans_id = models.IntegerField(
        _('AGR_TRANS_ID'),
        blank=True,
        null=True,
    )
    payment_vendor_trans_id = models.AutoField(
        _('ID'),
        primary_key=True
    )
    payment_merchant_trans_id = models.CharField(
        _('MERCHANT_TRANS_ID'),
        max_length=50,
        blank=True,
    )
    payment_merchant_trans_amount = models.IntegerField(
        _('MERCHANT_TRANS_AMOUNT'),
        db_index=True,
    )
    payment_status = models.IntegerField(
        _('STATUS'),
        choices=PaymentStatus.choices,
        blank=False,
        default=PaymentStatus.INITIATED,
    )
    payment_date = models.DateTimeField(
        _('DATE'),
        auto_now_add=True,
        db_index=True,
    )
    display_name = models.CharField(
        _('Display Name'),
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        _('Email'),
        max_length=80,
        null=False,
        blank=False,
    )
    phone_number = models.CharField(
        _('Phone number'),
        max_length=50,
        null=False,
        blank=True,
    )
    message = models.CharField(
        _('Message'),
        max_length=300,
        null=False,
        blank=True,
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name=_('Is Anonymous'),
    )
    is_gift = models.BooleanField(
        default=False,
        verbose_name=_('Is Gift'),
    )
    donation = models.ForeignKey(
        'Donation',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "PAYSYS Transaction"
        verbose_name_plural = "PAYSYS Transactions"


class Donation(models.Model):

    class PaymentMethods(models.IntegerChoices):
        PAYSYS = 1, _('PAYSYS')
        CLASSY = 2, _('CLASSY')
        OFFLINE = 3, _('OFFLINE')

    class PaymentCurrency(models.IntegerChoices):
        UZS = 1, _('UZS')
        USD = 2, _('USD')

    created = models.DateTimeField(
        _('Donation date'),
        auto_now_add=True,
        db_index=True,
    )
    amount = models.IntegerField(
        _('Amount'),
        db_index=True,
    )
    display_name = models.CharField(
        _('Display Name'),
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField(
        _('Email'),
        max_length=80,
        null=False,
        blank=False,
    )
    phone_number = models.CharField(
        _('Phone number'),
        max_length=50,
        null=False,
        blank=True,
    )
    message = models.CharField(
        _('Message'),
        max_length=300,
        null=False,
        blank=True,
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name=_('Is Anonymous'),
    )
    is_gift = models.BooleanField(
        default=False,
        verbose_name=_('Is Gift'),
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )
    payment_method = models.IntegerField(
        _('Payment method'),
        choices=PaymentMethods.choices,
        blank=False,
    )
    payment_currency = models.IntegerField(
        _('Payment currency'),
        choices=PaymentCurrency.choices,
        blank=False,
    )

    objects=DonationManager()

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"


class Ambassador(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=50,
    )
    description = models.TextField(
        _('Description'),
        max_length=1000,
    )
    avatar = models.ImageField(
        _('Avatar'),
        upload_to='ambassadors/',
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )

    class Meta:
        verbose_name = "Ambassador"
        verbose_name_plural = "Ambassadors"


class TeamMember(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=50,
    )
    description = models.TextField(
        _('Description'),
        max_length=1000,
    )
    avatar = models.ImageField(
        _('Avatar'),
        upload_to='team-members/',
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"


class Partner(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=300,
    )
    link = models.URLField(
        _('Link to Partner'),
        max_length=1000,
        blank=True,
    )
    is_link_enabled = models.BooleanField(
        default=False,
        verbose_name=_('Is Link Enabled'),
        db_index=True,
    )
    logo = models.ImageField(
        _('Logo'),
        upload_to='partners/',
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )

    class Meta:
        verbose_name = "Partner"
        verbose_name_plural = "Partners"


class GreenChampion(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=300,
    )
    link = models.URLField(
        _('Link to Green Champion'),
        max_length=1000,
        blank=True,
    )
    is_link_enabled = models.BooleanField(
        default=False,
        verbose_name=_('Is Link Enabled'),
        db_index=True,
    )
    logo = models.ImageField(
        _('Logo'),
        upload_to='green-champion/',
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )

    class Meta:
        verbose_name = "Green Champion"
        verbose_name_plural = "Green Champions"


class YouTubeLink(models.Model):
    description = models.CharField(
        _('Description'),
        max_length=100,
    )
    link = models.URLField(
        _('Video Link'),
        max_length=1000,
    )
    snapshot_width = models.IntegerField(
        _('Snapshot Width'),
    )
    snapshot_height = models.IntegerField(
        _('Snapshot Height'),
    )
    snapshot = models.ImageField(
        _('Snapshot'),
        upload_to='youtubelink-snapshot/',
        width_field='snapshot_width',
        height_field='snapshot_height',
        validators = [ImageDimensionsValidator(width=800, height=600)],
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )

    class Meta:
        verbose_name = "YouTube Link"
        verbose_name_plural = "YouTube Links"


class FAQ(models.Model):
    question = models.TextField(
        _('Question'),
        max_length=300,
    )
    answer = models.TextField(
        _('Answer'),
        max_length=1000,
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"


class LearnMore(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=300,
    )
    description = models.CharField(
        _('Description'),
        max_length=300,
    )
    link = models.URLField(
        _('Link'),
        max_length=1000,
    )
    background_image_width = models.IntegerField(
        _('Snapshot Width'),
    )
    background_image_height = models.IntegerField(
        _('Snapshot Height'),
    )
    background_image = models.ImageField(
        _('Background Image'),
        upload_to='learn-more-background/',
        width_field='background_image_width',
        height_field='background_image_height',
        validators = [ImageDimensionsValidator(width=800, height=800)],
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )

    class Meta:
        verbose_name = "Learn More Entry"
        verbose_name_plural = "Learn More Entries"


class USDRate(models.Model):
    rate = models.IntegerField(
        _('USD Rate'),
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )

    class Meta:
        verbose_name = "USD Rate"
        verbose_name_plural = "USD Rates"


class ClassyTransaction(models.Model):
    class PaymentStatus(models.TextChoices):
        SUCCESS = 'success', _('SUCCESS')
        INCOMPLETE = 'incomplete', _('INCOMPLETE')
        CANCELED = 'canceled', _('CANCELED')
        REFUNDED = 'refunded', _('REFUNDED')
        CB_INITIATED = 'cb_initiated', _('CB_INITIATED')
        CB_LOST = 'cb_lost', _('CB_LOST')
        TEST = 'test', _('TEST')

    raw_total_gross_amount= models.FloatField(
        _('raw_total_gross_amount'),
        db_index=True,
    )
    id = models.IntegerField(
        _('id'),
        primary_key=True,
        db_index=True,
    )
    status = models.CharField(
        _('status'),
        max_length=20,
        blank=False,
        choices=PaymentStatus.choices,
        default=PaymentStatus.CB_INITIATED,
    )
    created_at = models.DateTimeField(
        _('created_at'),
        db_index=True,
    )
    member_name = models.CharField(
        _('member_name'),
        max_length=50,
        null=False,
        blank=False,
    )
    member_email_address = models.EmailField(
        _('member_email_address'),
        max_length=80,
        null=False,
        blank=True,
    )
    member_phone = models.CharField(
        _('member_phone'),
        max_length=50,
        null=False,
        blank=True,
    )
    comment = models.CharField(
        _('comment'),
        max_length=300,
        null=False,
        blank=True,
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name=_('is_anonymous'),
    )
    is_gift_aid = models.BooleanField(
        default=False,
        verbose_name=_('is_gift_aid'),
    )
    donation = models.ForeignKey(
        'Donation',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = "CLASSY Transaction"
        verbose_name_plural = "CLASSY Transactions"


class NewsModel(models.Model):
    title = models.CharField(
        _('Title'),
        max_length=60,
    )
    description = models.TextField(
        _('Description'),
    )
    title_ru = models.CharField(
        _('Title (Russian)'),
        max_length=60,
        null=True,
        blank=True,
    )
    title_en = models.CharField(
        _('Title (English)'),
        max_length=60,
        null=True,
        blank=True,
    )
    title_uz = models.CharField(
        _('Title (Uzbek)'),
        max_length=60,
        null=True,
        blank=True,
    )
    description_ru = models.TextField(
        _('Description (Russian)'),
        null=True,
        blank=True,
    )
    description_en = models.TextField(
        _('Description (English)'),
        null=True,
        blank=True,
    )
    description_uz = models.TextField(
        _('Description (Uzbek)'),
        null=True,
        blank=True,
    )
    image = models.ImageField(
        _('Image'),
        upload_to='news/',
    )
    created = models.DateTimeField(
        _('Created Date'),
        auto_now_add=True,
        db_index=True,
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Creator'),
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is Published'),
        db_index=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News Entry"
        verbose_name_plural = "News Entries"