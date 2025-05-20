from django.urls import path
from django.urls import include

from .views import MostRecentDonationListView
from .views import MostAmountDonationListView
from .views import AmbassadorListView
from .views import TeamMemberListView
from .views import PartnerListView
from .views import YouTubeLinkListView
from .views import FAQListView
from .views import TotalDonationAmountView
from .views import GreenChampionListView
from .views import LearnMoreListView
from .views import NewsDetailView
from .views import RedirectView

from .views import PaySysTransactionCreateView
from .views import PaySysInfoView
from .views import PaySysPayView
from .views import PaySysNotifyView
from .views import PaySysCancelView
from .views import PaySysStatementView

from .views import ClassyTransactionCreateView
from .views import ClassyTransationLatestView
from .views import NewsModelListView

urlpatterns = [
    path(
        'donation/total/',
        TotalDonationAmountView.as_view(),
        name='donation-total',
    ),
    path(
        'donation/create/',
        PaySysTransactionCreateView.as_view(),
        name='paysys-transuctiondonation-create',
    ),
    path(
        'donation/list/most/recent/',
        MostRecentDonationListView.as_view(),
        name='donation-list-most-recent',
    ),
    path(
        'donation/list/most/amount/',
        MostAmountDonationListView.as_view(),
        name='donation-list-most-recent',
    ),
    path(
        'ambassador/list/',
        AmbassadorListView.as_view(),
        name='ambassador-list',
    ),
    path(
        'team-member/list/',
        TeamMemberListView.as_view(),
        name='team-member-list',
    ),
    path(
        'partner/list/',
        PartnerListView.as_view(),
        name='partner-list',
    ),
    path(
        'green-champion/list/',
        GreenChampionListView.as_view(),
        name='green-champion-list',
    ),
    path(
        'learn-more/list/',
        LearnMoreListView.as_view(),
        name='learn-more-list',
    ),
    path(
        'youtube-link/list/',
        YouTubeLinkListView.as_view(),
        name='youtube-link-list',
    ),
    path(
        'faq/list/',
        FAQListView.as_view(),
        name='faq-list',
    ),
    path(
        'paysys/info/',
        PaySysInfoView.as_view(),
        name='paysys-info',
    ),
    path(
        'paysys/pay/',
        PaySysPayView.as_view(),
        name='paysys-pay',
    ),
    path(
        'paysys/notify/',
        PaySysNotifyView.as_view(),
        name='paysys-notify',
    ),
    path(
        'paysys/cancel/',
        PaySysCancelView.as_view(),
        name='paysys-cancel',
    ),
    path(
        'paysys/statement/',
        PaySysStatementView.as_view(),
        name='paysys-statement',
    ),
    path(
        'classy/create/',
        ClassyTransactionCreateView.as_view(),
        name='classy-transaction-create',
    ),
    path(
        'classy/latest/',
        ClassyTransationLatestView.as_view(),
        name='classy-transaction-latest-id',
    ),

    path(
        'news/list/',
        NewsModelListView.as_view(),
        name='news-list',
    ),
    path(
        'news/detail/<int:pk>/',
        NewsDetailView.as_view(),
        name='news-detail',
    ),

    path(
        'redirect/',
        RedirectView.as_view(),
        name='redirect',
    ),
]
