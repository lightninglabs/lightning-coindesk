from coindesk import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin

import grpc
import sys


class Profile(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    handle = models.CharField(max_length=30)
    identity_pubkey = models.CharField(max_length=80, unique=True)
    # bitcoin_address = BitcoinAddressField()


class Article(models.Model):

    ARTICLE_STATUS_CHOICES = (
        ('visible', 'Visible'),
        ('deleted by admin', 'Deleted by admin'),
    )

    title = models.CharField(max_length=191)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='visible', choices=ARTICLE_STATUS_CHOICES)

    def views(self):
        return self.payments.filter(status='complete', purpose='view').count()

    def upvotes(self):
        return self.payments.filter(status='complete', purpose='upvote').count()

    def __str__(self):
        return "({}) '{}'".format(self.id, self.title)

    def upvote(self, upvoter, amount):
        # TODO Implement
        pass


class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ('pending_invoice', 'Pending Invoice'), # Should be atomic
        ('pending_payment', 'Pending Payment'),
        ('complete', 'Complete'),
        ('error', 'Error'),
    )

    PAYMENT_PURPOSE_CHOICES = (
        ('view', 'View'),
        ('upvote', 'Upvote')
    )

    user = models.ForeignKey(User)
    article = models.ForeignKey(Article, related_name='payments')
    purpose = models.CharField(max_length=10, choices=PAYMENT_PURPOSE_CHOICES)

    satoshi_amount = models.IntegerField()
    r_hash = models.CharField(max_length=64)
    payment_request = models.CharField(max_length=1000)

    status = models.CharField(max_length=50, default='pending_invoice', choices=PAYMENT_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def generate_invoice(self, user, article):
        assert self.status == 'pending_invoice', "Already generated invoice"
        channel = grpc.insecure_channel(settings.LND_RPCHOST)
        stub = lnrpc.LightningStub(channel)
        try:
            invoice_response = stub.AddInvoice(ln.Invoice(value=1000, memo="User '{}' | ArticleId {}".format(user.username, article.id)))
            # Have to decode with ancient MS-DOS codec since it's the only one that works with random bytestrings
            self.r_hash = invoice_response.r_hash.decode('cp437')
            self.payment_request = invoice_response.payment_request
            self.status = 'pending_payment'
            self.save()
        except Exception:
            t, v, tb = sys.exc_info()
            raise t, v, tb


admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(Article)
