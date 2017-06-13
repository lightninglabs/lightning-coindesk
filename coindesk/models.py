from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Profile(models.Model):
    user = models.OneToOneField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    handle = models.CharField(max_length=30)
    identity_pubkey = models.CharField(max_length=80, unique=True)
    # lightning_address = BitcoinAddressField()


class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = (
        ('pending_invoice', 'Pending Invoice'),
        ('pending_payment', 'Pending Payment'),
        ('complete', 'Complete'),
        ('error', 'Error'),
    )

    sender = models.ForeignKey(User, related_name='senders')
    recipient = models.ForeignKey(User, related_name='recipients')
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default='accepted', choices=PAYMENT_STATUS_CHOICES)
    r_hash = models.CharField(max_length=64)
    payment_req = models.CharField(max_length=1000)

admin.site.register(Profile)
admin.site.register(Payment)
