from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from user.forms import SignupForm, LeaveReviewForm, ProfileForm, UserMerchantOnlyForm
from django.contrib import messages
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from user.models import Profile, Reviews
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
# Create your views here.
def index(request):
    return HttpResponse('this is the index for "user/"')


# this view could definitely be optimized.
def profile(request, user_id=None):
    try:
        usercontext = User.objects.get(username=user_id)
        # refactored code so that reviewscores are directly saved in the models.(receiver updates it.)
        percentscore = usercontext.profile.reviewscore
        # GET REVIEWS ASSOCIATED WITH USER.
        reviews = Reviews.objects.filter(review_to=usercontext).order_by('-review_date')

        # unique case where 1 bad review does not make your score appear red.
        # bad logic
    except User.DoesNotExist:
        usercontext = None
        percentscore = None
        textstyle = None
        reviews = None

    context = {'user':usercontext, 'score':percentscore, 'reviews':reviews, 'showeditprofile':False}
    return render(request, 'user/userprofile.html', context)


@login_required
def own_profile(request):
    if request.user.is_authenticated:
        usercontext = request.user
        reviews = Reviews.objects.filter(review_to=usercontext).order_by('-review_date')
        percentscore = usercontext.profile.reviewscore
    else:
        usercontext = True
        percentscore = None
        reviews = None
    context = {'user':usercontext, 'score':percentscore, 'reviews':reviews, 'showeditprofile':True}
    return render(request, 'user/userprofile.html', context)

@login_required
@transaction.atomic
def editprofile(request):
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_get_ms_info = User.objects.get(username=request.user.username)
        user_merchant_only_form = UserMerchantOnlyForm(request.POST, instance=request.user, ms_kw=user_get_ms_info)
        if profile_form.is_valid() and user_merchant_only_form.is_valid():
            user_merchant_only_form.save()
            profile_form.save()
            return redirect('user:browseownprofile')
        else:
            context = {'form' : profile_form, 'userform':user_merchant_only_form, 'user':request.user}
            return render(request, 'user/editprofile.html', context)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_merchant_only_form = UserMerchantOnlyForm(instance=request.user)
        context = {'form' : profile_form, 'userform':user_merchant_only_form, 'user':request.user}
        return render(request, 'user/editprofile.html',context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            user_try_login = login(request, user)
            return redirect('accounts:index')
        else:
            messages.error(request, "Please check the fields.")
    else:
        form = SignupForm()
    context = {'form':form}
    return render(request, 'user/signup.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        context = None
        if form.is_valid():
            #login user
            user = form.get_user()
            login(request, user)
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
        if request.user.is_authenticated:
            usercontext = request.user
            context = usercontext
            print(context)
        else:
            context = None

    context_dic = {'form':form, 'context':context}

    return render(request, "user/login.html", context_dic)


@login_required
def userlogout(request):
    logout(request)
    return redirect('indexhome')

@login_required
def review(request, slug):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = LeaveReviewForm(data=request.POST, user_to = slug, contextuser = request.user.username)
            if form.is_valid():
                return_to = form.cleaned_data['review_to']
                review_type = form.cleaned_data['review_type']
                # IF USER CHOOSES NEGATIVE REVIEW, INCREASE BAD_REVIEW_COUNT.
                form.save()
                return redirect(reverse('user:browseotherprofile', kwargs={'user_id':return_to.username}))
        if request.method == 'GET':
            form = LeaveReviewForm(data=request.POST, user_to = slug, contextuser = request.user.username)
            try:
                user = User.objects.filter(username=slug)
            except User.DoesNotExist:
                raise Http404
            context = {'form':form}
            return render(request, "user/leave_review.html", context)
    else:
        context = {'nologin':'You need to be logged in to do that.'}
        return render(request, "user/leave_review.html", context)