import csv

from django.contrib import admin
from django.db.models import TextField
from django.utils.html import mark_safe

from tinymce.widgets import TinyMCE

from .models import Donation
from .models import Ambassador
from .models import TeamMember
from .models import Partner
from .models import GreenChampion
from .models import YouTubeLink
from .models import FAQ
from .models import USDRate
from .models import LearnMore
from .models import PaySysTransaction
from .models import ClassyTransaction
from .models import NewsModel


class DonationAdmin(admin.ModelAdmin):
    search_fields = ['display_name', 'email', 'payment_method', 'amount']
    list_display = (
        'display_name',
        'amount',
        'payment_method',
        'created'
    )
    list_filter = ['created', 'payment_method', 'amount']
    exclude = ('creator', 'payment_method')

    def save_model(self, request, obj, form, change):
        obj.payment_method = Donation.PaymentMethods.OFFLINE
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class AmbassadorAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = (
        'name',
        'description',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator',)

    readonly_fields = ['current_avatar']

    def current_avatar(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.avatar.url,
                width=obj.avatar.width,
                height=obj.avatar.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_avatar')
        return fields

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class TeamMemberAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = (
        'name',
        'description',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator',)

    readonly_fields = ['current_avatar']

    def current_avatar(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.avatar.url,
                width=obj.avatar.width,
                height=obj.avatar.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_avatar')
        return fields

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class GreenChampionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = (
        'name',
        'link',
        'is_link_enabled',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator',)

    readonly_fields = ['current_logo']

    def current_logo(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.logo.url,
                width=obj.logo.width,
                height=obj.logo.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_logo')
        return fields

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class PartnerAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = (
        'name',
        'link',
        'is_link_enabled',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator',)

    readonly_fields = ['current_logo']

    def current_logo(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.logo.url,
                width=obj.logo.width,
                height=obj.logo.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_logo')
        return fields

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class YouTubeLinkAdmin(admin.ModelAdmin):
    search_fields = ['description']
    list_display = (
        'description',
        'link',
        'created',
        'creator',
        'snapshot_width',
        'snapshot_height',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator', 'snapshot_width', 'snapshot_height',)

    readonly_fields = ['current_snapshot']

    def current_snapshot(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.snapshot.url,
                width=obj.snapshot.width,
                height=obj.snapshot.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_snapshot')
        return fields

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class LearnMoreAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
    list_display = (
        'title',
        'description',
        'link',
        'background_image_width',
        'background_image_height',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator', 'background_image_width', 'background_image_height',)

    readonly_fields = ['current_background_image']

    def current_background_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.current_background_image.url,
                width=obj.current_background_image.width,
                height=obj.current_background_image.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_background_image')
        return fields

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class FAQAdmin(admin.ModelAdmin):
    search_fields = ['question', 'answer']
    list_display = (
        'question',
        'answer',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator',)

    actions = ["publish", "unpublish"]

    formfield_overrides = {
        TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class USDRateAdmin(admin.ModelAdmin):
    list_display = (
        'rate',
        'created',
        'creator',
    )
    list_filter = ['created']
    exclude = ('creator',)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


class PaySysTransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('payment_vendor_trans_id',)
    list_display = (
        'payment_vendor_trans_id',
        'payment_merchant_trans_amount',
        'display_name',
        'payment_status',
        'payment_date',
    )
    list_filter = ['payment_date', 'payment_status']


class ClassyTransactionAdmin(admin.ModelAdmin):
    search_fields = ['member_name', 'status']
    readonly_fields = ('id',)
    list_display = (
        'id',
        'raw_total_gross_amount',
        'member_name',
        'status',
        'created_at',
    )
    list_filter = ['created_at']


class NewsModelAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title', 'title_ru', 'title_en', 'title_uz']
    list_display = (
        'id',
        'title',
        'description',
        'created',
        'creator',
        'is_published',
    )
    list_filter = ['created', 'is_published']
    exclude = ('creator',)

    readonly_fields = ['current_image']
    actions = ["publish", "unpublish"]

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'is_published', 'current_image')
        }),
        ('Русская версия', {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        ('English version', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Uzbek versiya', {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
    )

    def current_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.image.url,
                width=obj.image.width,
                height=obj.image.height,
            )
        )

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:
            fields.remove('current_image')
        return fields

    def publish(self, request, queryset):
        queryset.update(is_published=True)

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Donation, DonationAdmin)
admin.site.register(Ambassador, AmbassadorAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(GreenChampion, GreenChampionAdmin)
admin.site.register(YouTubeLink, YouTubeLinkAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(USDRate, USDRateAdmin)
admin.site.register(LearnMore, LearnMoreAdmin)
admin.site.register(PaySysTransaction, PaySysTransactionAdmin)
admin.site.register(ClassyTransaction, ClassyTransactionAdmin)
admin.site.register(NewsModel, NewsModelAdmin)

admin.site.site_header = "GreenAralSea.org Admin"
admin.site.site_title = "GreenAralSea.org Portal"
admin.site.index_title = "Welcome to GreenAralSea.org Portal"
