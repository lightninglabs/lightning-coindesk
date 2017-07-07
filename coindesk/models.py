from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin

import codecs


class Profile(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
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

    @property
    def views(self):
        return self.payments.filter(status='complete', purpose='view').count()

    @property
    def upvotes(self):
        raise NotImplementedError()
        return self.payments.filter(status='complete', purpose='upvote').count()

    def __str__(self):
        return "({}) '{}'".format(self.id, self.title)

    def upvote(self, upvoter, amount):
        raise NotImplementedError()


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
        """
        Generates a new invoice
        """
        pass

    def check_payment(self):
        """
        Checks if the Lightning payment has been received for this invoice
        """
        pass

admin.site.register(Profile)
admin.site.register(Payment)
admin.site.register(Article)
