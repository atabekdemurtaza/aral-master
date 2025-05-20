from hashlib import md5
from datetime import datetime

from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.db import transaction as db_transaction
from django.http import Http404

from rest_framework import status
from rest_framework import views
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from api.models import Donation
from api.models import ClassyTransaction

from api.serializers import ClassyTransactionSerializer




def ms_to_datetime(ms):
    return datetime.fromtimestamp(ms/1000)


def get_epoch_time(str_dt):
    dt = parse_datetime(str_dt).replace(tzinfo=None)
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds() * 1000.0)


class ClassyTransactionCreateView(views.APIView):

    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return ClassyTransaction.objects.get(pk=pk)
        except ClassyTransaction.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        transaction = ClassyTransaction.objects.filter(
            id=request.data['id'],
        ).first()

        if transaction is None:
            serializer = ClassyTransactionSerializer(
                data=request.data
            )
        else:
            serializer = ClassyTransactionSerializer(
                transaction,
                data=request.data
            )

        serializer.is_valid(raise_exception=True)
        transaction = serializer.save()

        with db_transaction.atomic():
            if transaction.status == ClassyTransaction.PaymentStatus.SUCCESS and transaction.donation is None:
                donation = Donation.objects.create(
                    amount=transaction.raw_total_gross_amount,
                    display_name=transaction.member_name,
                    email=transaction.member_email_address,
                    phone_number=transaction.member_phone,
                    message=transaction.comment,
                    is_anonymous=transaction.is_anonymous,
                    is_gift=transaction.is_gift_aid,
                    payment_method=Donation.PaymentMethods.CLASSY,
                    payment_currency=Donation.PaymentCurrency.USD,
                )
                transaction.donation = donation
                transaction.save()
            else:
                if transaction.status != ClassyTransaction.PaymentStatus.SUCCESS and transaction.donation is not None:
                    donation_id = transaction.donation.id
                    transaction.donation = None
                    transaction.save()
                    Donation.objects.get(pk=donation_id).delete()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassyTransationLatestView(views.APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        transaction = ClassyTransaction.objects.earliest('id')
        return Response(
            {
                'id': transaction.id,
            },
            status=status.HTTP_200_OK,
        )
