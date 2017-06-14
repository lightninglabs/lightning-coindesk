from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render
from coindesk.models import Article, Payment, Profile


def index(request):
    articles = Article.objects.all()[:25]
    articles = sorted(articles, key=lambda p: p.value, reverse=True)
    context = {'articles': articles}

    # TODO code to check if the user is authenticated or not.
    if request.user.is_authenticated():
        lnd_user = request.user
    else:
        lnd_user = None

    if lnd_user is not None:
        context['lnd_user'] = lnd_user
        context['profile'] = lnd_user.profile

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


def pay_for_view(request, pk):
    # TODO implement payments

    if not request.user.is_authenticated():
        raise Exception("Must be logged in to make payment")

    return HttpResponseRedirect("/")


def upvote(request, pk):
    # TODO implement payments

    if not request.user.is_authenticated():
        raise Exception("Must be logged in to upvote")

    return HttpResponseRedirect("/")
