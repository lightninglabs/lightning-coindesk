from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from coindesk.models import Payment, Profile


def index(request):
    # payments = Payment.objects.all()[:25]
    # payments = sorted(payments, key=lambda p: p.value, reverse=True)
    # context = {'payments': payments, 'user': request.user, }
    # try:
    #     lnd_user = User.objects.get(profile__identity_pubkey=settings.LND_IDENTITY_PUBKEY)
    # except User.DoesNotExist:
    #     lnd_user = None

    # if lnd_user is not None:
    #     context['lnd_user'] = lnd_user
    #     context['profile'] = lnd_user.profile

    return render_to_response(
        template_name='index.html',
        # context=context)
        context={})


def profile(request, username):
    user = User.objects.get(username='phlip9')
    _profile = Profile.objects.get(user=user)
    return render_to_response(
        template_name='profile.html',
        context = {'user': user, 'profile': _profile})


def upvote(request, pk):
    if not request.user.is_authenticated():
        raise Exception("Must be logged in to upvote")

    payment = Payment.objects.get(id=pk)
    amount = int(request.GET.get('amount', 0))
    payment.upvote(request.user, amount)

    return HttpResponseRedirect("/")


def create_post(request):

    title = request.GET.get('title', "(No title)")
    link = request.GET.get('link', "http://maxfa.ng")

    print title, link # TODO remove
    # TODO
    # p = Payment(curator=request.user,
    #          title=title,
    #          link=link)
    # p.save()
    # p.upvote(request.user, 100)  # Costs 100 satoshi to post

    return HttpResponseRedirect("/")


def submit(request):
    user = User.objects.get(username='phlip9')
    _profile = Profile.objects.get(user=user)
    return render_to_response(
        template_name='submit.html',
        context={'user': user, 'profile': _profile})
