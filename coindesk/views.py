from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render
from coindesk.models import Article, Profile


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
        payment_status = None
    elif qs.count() == 1:
        payment_status = qs.last().status
        if payment_status == 'error':
            # TODO Implement some kind of error resolution
            pass
            raise Exception("Payment error")
        elif payment_status == 'pending_invoice':
            # This should not happen because invoice generation should happen immediately
            raise Exception("Invoice not generated for view")
        else:
            context['payment_status'] = payment_status
    else:
        # This should not happen because there should never be more than one view payment per article per person
        raise Exception("Multiple payment")

    # TODO Remove this when payments is fully integrated
    context['payment_status'] = 'complete'

    return render(request,
        template_name='article.html',
        context=context)


def pay_for_view(request, pk):
    # TODO implement payments

    if not request.user.is_authenticated():
        raise Exception("Must be logged in to make payment")

    return HttpResponseRedirect("/")


def upvote(request, pk):
    # TODO implement payments

    article = Article.objects.get(id=pk)
    amount = int(request.GET.get('amount', 0))
    article.upvote(request.user, amount)

    if not request.user.is_authenticated():
        raise Exception("Must be logged in to upvote")

    return HttpResponseRedirect("/")
