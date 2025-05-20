from hashlib import md5
from datetime import datetime

from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.db import transaction as db_transaction

from rest_framework import status
from rest_framework import views
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import Donation
from api.models import PaySysTransaction

from api.serializers import PaySysTransactionCreateSerializer


ERRORS = [
    {
        "ERROR": 0,
        "ERROR_NOTE": "",
        "PARAMETERS": {},
    },
    {
        "ERROR": -1,
        "ERROR_NOTE": "SIGN CHECK FAILED!",
    },
    {
        "ERROR": -2,
        "ERROR_NOTE": "Incorrect paramter amount",
    },
    {
        "ERROR": -3,
        "ERROR_NOTE": "Not enough parameters",
    },
    {
        "ERROR": -4,
        "ERROR_NOTE": "Already paid",
    },
    {
        "ERROR": -5,
        "ERROR_NOTE": "The order does not exist"
    },
    {
        "ERROR": -6,
        "ERROR_NOTE": "The transaction does not exist"
    },
    {
        "ERROR": -7,
        "ERROR_NOTE": "Failed to update user",
    },
    {
        "ERROR": -8,
        "ERROR_NOTE": "Error in request"
    },
    {
        "ERROR": -9,
        "ERROR_NOTE": "Transaction cancelled",
    },
    {
        "ERROR": -10,
        "ERROR_NOTE": "The vendor is not found",
    },
]


def ms_to_datetime(ms):
    return datetime.fromtimestamp(ms/1000)


def get_epoch_time(str_dt):
    dt = parse_datetime(str_dt).replace(tzinfo=None)
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000.0)


class PaySysTransactionCreateView(generics.CreateAPIView):
    queryset = PaySysTransaction.objects.all()
    serializer_class = PaySysTransactionCreateSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        if 'amount' in request.data:
            request.data['payment_merchant_trans_amount'] = request.data['amount']

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        sign_time = get_epoch_time(serializer.data.get('payment_date'))
        sign_string = md5(
            ''.join(map(str,
                    [
                        settings.PAYSYS_SECRET_KEY,
                        settings.PAYSYS_VENDOR_ID,
                        serializer.data.get('payment_vendor_trans_id'),
                        serializer.data.get('payment_merchant_trans_amount'),
                        'sum',
                        sign_time,
                    ]
                )
            ).encode()
        ).hexdigest()
        return Response(
            {
                'VENDOR_ID': settings.PAYSYS_VENDOR_ID,
                'MERCHANT_TRANS_ID': serializer.data['payment_vendor_trans_id'],
                'MERCHANT_TRANS_AMOUNT': serializer.data['payment_merchant_trans_amount'],
                'MERCHANT_CURRENCY': 'sum',
                'MERCHANT_TRANS_NOTE': '',
                'MERCHANT_TRANS_DATA': '',
                'MERCHANT_TRANS_RETURN_URL': 'https://greenaralsea.org/',
                'SIGN_TIME': sign_time,
                'SIGN_STRING': sign_string,
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class PaySysMixin(object):
    permission_classes = (AllowAny,)

    def handle_exception(self, exc):
        response = super(PaySysMixin, self).handle_exception(exc)
        return Response(ERRORS[8]) if response.status_code == 406 else response


class PaySysStatementView(PaySysMixin, views.APIView):
    def post(self, request, *args, **kwargs):
        KEYWORDS = ['FROM', 'TO', 'SIGN_TIME', ]
        ALL = KEYWORDS + ['SIGN_STRING', ]

        if any([key not in request.data for key in ALL]):
            return Response(ERRORS[3])

        calculated_sign_string = md5(
            ''.join(map(str,
                    [settings.PAYSYS_SECRET_KEY,] + [
                        request.data[key] for key in KEYWORDS
                    ]
                )
            ).encode()
        ).hexdigest()

        if request.data['SIGN_STRING'] != calculated_sign_string:
            return Response(ERRORS[1])

        datetime_from = ms_to_datetime(int(request.data['FROM']))
        datetime_to = ms_to_datetime(int(request.data['TO']))

        transactions = PaySysTransaction.objects.filter(
            payment_date__range=[datetime_from, datetime_to]
        )

        return Response(
            {
                "ERROR": 0,
                "ERROR_NOTE": "Success",
                "TRANSACTIONS": [],
            }
        )


class PaySysCancelView(PaySysMixin, views.APIView):
    def post(self, request, *args, **kwargs):
        KEYWORDS = ['AGR_TRANS_ID', 'VENDOR_TRANS_ID', 'SIGN_TIME', ]
        ALL = KEYWORDS + ['SIGN_STRING', ]

        if any([key not in request.data for key in ALL]):
            return Response(ERRORS[3])

        calculated_sign_string = md5(
            ''.join(map(str,
                    [settings.PAYSYS_SECRET_KEY,] + [
                        request.data[key] for key in KEYWORDS
                    ]
                )
            ).encode()).hexdigest()

        if request.data['SIGN_STRING'] != calculated_sign_string:
            return Response(ERRORS[1])

        transaction = PaySysTransaction.objects.filter(
            payment_vendor_trans_id=request.data['VENDOR_TRANS_ID']
        ).first()
        if transaction is None:
            return Response(ERRORS[6])

        return Response(
            {
                "ERROR": 0,
                "ERROR_NOTE": "Success",
            }
        )


class PaySysNotifyView(PaySysMixin, views.APIView):
    def post(self, request, *args, **kwargs):
        KEYWORDS = [
            'AGR_TRANS_ID', 'VENDOR_TRANS_ID', 'STATUS', 'SIGN_TIME',
        ]
        ALL = KEYWORDS + [
            'SIGN_STRING',
        ]

        if any([key not in request.data for key in ALL]):
            return Response(ERRORS[3])

        calculated_sign_string = md5(
            ''.join(map(str,
                    [settings.PAYSYS_SECRET_KEY,] + [
                        request.data[key] for key in KEYWORDS
                    ]
                )
            ).encode()
        ).hexdigest()

        if request.data['SIGN_STRING'] != calculated_sign_string:
            return Response(ERRORS[1])

        transaction = PaySysTransaction.objects.filter(
            payment_vendor_trans_id=request.data['VENDOR_TRANS_ID']
        ).first()
        if transaction is None:
            return Response(ERRORS[6])

        with db_transaction.atomic():
            if request.data['STATUS'] == PaySysTransaction.PaymentStatus.PAYED:
                donation = Donation.objects.create(
                    amount=transaction.payment_merchant_trans_amount,
                    display_name=transaction.display_name,
                    email=transaction.email,
                    phone_number=transaction.phone_number,
                    message=transaction.message,
                    is_anonymous=transaction.is_anonymous,
                    is_gift=transaction.is_gift,
                    payment_method=Donation.PaymentMethods.PAYSYS,
                    payment_currency=Donation.PaymentCurrency.UZS,
                )
                transaction.donation = donation
            elif request.data['STATUS'] == PaySysTransaction.PaymentStatus.CANCELED:
                if transaction.donation is not None:
                    donation_id = transaction.donation.id
                    transaction.donation = None
                    transaction.save()
                    Donation.objects.get(pk=donation_id).delete()
            transaction.payment_status = request.data['STATUS']
            transaction.save()

        return Response(
            {
                "ERROR": 0,
                "ERROR_NOTE": "Success",
            }
        )


class PaySysPayView(PaySysMixin, views.APIView):
    def post(self, request, *args, **kwargs):
        KEYWORDS = [
            'AGR_TRANS_ID', 'VENDOR_ID', 'PAYMENT_ID', 'PAYMENT_NAME',
            'MERCHANT_TRANS_ID', 'MERCHANT_TRANS_AMOUNT', 'ENVIRONMENT',
            'SIGN_TIME',
        ]
        OPTIONAL = [
            'MERCHANT_TRANS_DATA',
        ]
        ALL = KEYWORDS + [
            'SIGN_STRING',
        ]

        if any([key not in request.data for key in ALL]):
            return Response(ERRORS[3])

        calculated_sign_string = md5(
            ''.join(map(str,
                    [settings.PAYSYS_SECRET_KEY,] + [
                        request.data[key] for key in KEYWORDS
                    ]
                )
            ).encode()
        ).hexdigest()

        if request.data['SIGN_STRING'] != calculated_sign_string:
            return Response(ERRORS[1])

        transaction = PaySysTransaction.objects.filter(
            payment_vendor_trans_id=request.data['MERCHANT_TRANS_ID']
        ).first()

        if transaction is None:
            return Response(ERRORS[5])

        if transaction.payment_merchant_trans_amount != request.data['MERCHANT_TRANS_AMOUNT']:
            return Response(ERRORS[2])

        if transaction.payment_status == PaySysTransaction.PaymentStatus.PAYED:
            return Response(ERRORS[4])

        return Response(
            {
                "ERROR": 0,
                "ERROR_NOTE": "Success",
                "VENDOR_TRANS_ID": transaction.payment_vendor_trans_id,
            }
        )


class PaySysInfoView(PaySysMixin, views.APIView):
    def post(self, request, *args, **kwargs):

        merchant_trans_id = request.data.get('MERCHANT_TRANS_ID', None)
        sign_time = request.data.get('SIGN_TIME', None)
        sign_string = request.data.get('SIGN_STRING', None)

        if merchant_trans_id is None or \
           sign_time is None or \
           sign_string is None:
            return Response(ERRORS[3])

        calculated_sign_string = md5(
            ''.join(map(str,
                [
                    settings.PAYSYS_SECRET_KEY,
                    merchant_trans_id,
                    sign_time,
                ]
            )
        ).encode()).hexdigest()

        if sign_string != calculated_sign_string:
            return Response(ERRORS[1])

        transaction = PaySysTransaction.objects.filter(
            payment_vendor_trans_id=merchant_trans_id,
        ).first()
        if transaction is None:
            return Response(ERRORS[5])

        return Response(
            {
                "ERROR": 0,
                "ERROR_NOTE": "Success",
                "PARAMETERS": {
                    "name": transaction.display_name,
                    "email": transaction.email,
                    "amount": transaction.payment_merchant_trans_amount,
                }
            }
        )
