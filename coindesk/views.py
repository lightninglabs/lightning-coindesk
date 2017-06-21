from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render
from coindesk.models import Article, Profile, Payment


def index(request):
    articles = Article.objects.all()[:25]
    articles = sorted(articles, key=lambda p: p.upvotes, reverse=True)
    context = {'articles': articles}

    if request.user.is_authenticated():
        context['profile'], _ = Profile.objects.get_or_create(user=request.user)

    return render(request,
        template_name='index.html',
        context=context)


def login(request):
    # Repurpose the CSRF token as the message the user needs to sign
    csrf_token = get_token(request)
    context = {'csrf_token': csrf_token}
    return render(request,
            template_name='login.html',
            context=context)


def verify(request):

    # TODO Verify signature

    return render(request,
        template_name='index.html',
        context={})


@login_required
def profile(request, username):
    _profile = Profile.objects.get(user=request.user)
    return render(request,
        template_name='profile.html',
        context = {'user': request.user, 'profile': _profile})


def article(request, pk):

    if not request.user.is_authenticated():
        raise Exception("You must be logged in to view an article!")

    try:
        article = Article.objects.filter(status='visible').get(id=pk)
    except Article.DoesNotExist:
        raise Exception("Article with id {} does not exist or is not visible".format(pk))

    context = {'article': article}

    qs = article.payments.filter(user=request.user, purpose='view')

    if qs.count() == 0:
        # Generate a new payment
        payment, _ = Payment.objects.get_or_create(user=request.user,
                          article=article,
                          purpose='view',
                          satoshi_amount=settings.MIN_VIEW_AMOUNT,
                          status='pending_invoice')
        payment.save()
    elif qs.count() == 1:
        payment = qs.last()
    else:
        # This should not happen because there should never be more than one view payment per article per person
        raise Exception("Multiple payments detected")

    # User client requests that we check if the payment has been made
    if request.GET.get('check'):
        print "Checking for payment {}".format(payment.payment_request)
        if payment.check_payment():
            print "Payment succeeded!"
        else:
            print "Payment not received"

    if payment.status == 'pending_invoice':
        payment.generate_invoice(request.user, article)
    elif payment.status == 'pending_payment':
        # Do nothing; display the payment page to user
        pass
    elif payment.status == 'complete':
        # Do nothing; display the article to user
        pass
    elif payment.status == 'error':
        # TODO Optionally implement some kind of error resolution
        pass
        raise Exception("Payment error")
    else:
        context['payment_status'] = payment.status

    context['payment'] = payment

    return render(request,
        template_name='article.html',
        context=context)


def upvote(request, pk):
    # TODO implement payments

    article = Article.objects.get(id=pk)
    amount = int(request.GET.get('amount', 0))
    article.upvote(request.user, amount)

    if not request.user.is_authenticated():
        raise Exception("Must be logged in to upvote")

    return HttpResponseRedirect("/")
