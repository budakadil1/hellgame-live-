from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.urls import reverse
from .models import gameIdentifier, gamePost
from user.models import Profile, CustomUser
from django.views.generic.detail import DetailView
from django.views.decorators.cache import never_cache
from .filters import PostFilter, GameFilter
from accounts.forms import ListingForm, EditListingForm
from user.models import CustomUser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

def index(request):
    try:
        games = gameIdentifier.objects.all()
        gameFilter = GameFilter(request.GET, queryset=games)
        gameFilter_qs = gameFilter.qs.order_by('game_name')
    except:
        exception = "No objects"
        return render(request, 'accounts/all_categories.html', {'exception':exception})
    
    return render(request, 'accounts/all_categories.html',{'games':gameFilter_qs, 'filter':gameFilter})

# LIST INDIVIDUAL POSTS BY GAMES SUCH AS /accounts/lol or /accounts/brawlhalla
def category_detail(request, slug):
    # is this fine performance-wise ? probably not.
    template = 'accounts/category_detail.html'
    category = get_object_or_404(gameIdentifier, game_slug=slug)
    # ADDED DOUBLEFILTERS TO NOT PASS HIDDEN (MERCHANT_STATUS = DISABLED USER'S POSTS.)
    post = gamePost.objects.filter(post_category=category).filter(posted_by__merchant_status=True)
    postFilter = PostFilter(request.GET, queryset=post)
    postFilter_qs = postFilter.qs.order_by('-date')
    paginator = Paginator(postFilter_qs, 12)
    page = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    if postFilter_qs.exists():
        context = {
        'page_obj':page_obj,
        'category':category,
        'filter':postFilter,
    }
    else:
        context = {
        'page_obj':page_obj,
        'category':category,
        'filter':postFilter,
    }
    return render(request, template, context)

# list my listings.
@login_required
def my_listings(request):
    template = 'accounts/mylistings.html'
    post = gamePost.objects.filter(posted_by=request.user).order_by('-date')
    paginator = Paginator(post, 12)
    page = request.GET.get('page')
    user = request.user
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    if post.exists() and user.merchant_status == True:
        context={
            'post':post,
            'page_obj':page_obj,
            'None':False,
            'user':user,
        }
    else:
        context={
            'post':None,
            'page_obj':None,
            'None':True,
            'user':user,
        }
    return render(request, template, context)


def game_category_list(request, slug):
    template = 'accounts/game_category_list.html'
    post = get_list_or_404(gameIdentifier, game_choice=slug)
    for game in post:
        category = game.game_choice
    context = {
    'post':post,
    'category':category,
    }
    return render(request, template, context)


def product_view(request, slug):
    template = 'accounts/game_product_view.html'
    post = get_list_or_404(gamePost, slug=slug)
    for i in post:
        user = i.posted_by
    usercontext = Profile.objects.get(user=user)
    reviewscore = usercontext.reviewscore
    context = {'post':post, 'reviewscore':reviewscore}
    return render(request, template, context)


@login_required
def add_listing(request):
    # check if user is logged in.
    if request.user.is_authenticated:
        # if user is logged in, check to see if they have merchant_status = True on their information.
        contextuser = CustomUser.objects.get(username=request.user.username)
        if contextuser.merchant_status == True:
            if request.method == 'GET':
                form = ListingForm(user=request.user.username)
                context = {'nomerchantstatus':False, 'form':form}
                return render(request, 'accounts/add-listing.html', context)
            if request.method == 'POST':
                form = ListingForm(request.POST, user=request.user.username)
                if form.is_valid():
                    category = form.cleaned_data['post_category'].game_slug
                    form.save()
                    return redirect(reverse('accounts:game_category',kwargs={'slug':category}))
                else:
                    context = {'nomerchantstatus':False, 'form':form}
                    return render(request, 'accounts/add-listing.html',context)
        elif contextuser.merchant_status == False:
            if request.method == 'GET':
                context = {'nomerchantstatus' : True}
                return render(request, 'accounts/add-listing.html', context)

    else:
        context = {'nologin':'You need to be logged in to do that.'}
        return render(request, 'accounts/add-listing.html', context)


@login_required
def edit_listing(request, slug):
    # check if user is logged in.
    if request.user.is_authenticated:
        if request.method == 'GET':
            # check if user is the actual poster of the listing and if the listing exists. if yes, assign as instance.
            try:
                check = gamePost.objects.get(slug=slug)
                if check.posted_by == request.user:
                    instance = check
                    form = EditListingForm(instance=instance)
                    context = {'form':form}
                elif check.posted_by != request.user:
                    context = {'notowner':True}
                return render(request, 'accounts/editlisting.html', context)
            except gamePost.DoesNotExist:
                return render(request, 'accounts/editlisting.html', {'NoListingFound':'No such listing found.'})
        # check again for postman-like attacks?
        if request.method == 'POST':
            check = gamePost.objects.get(slug=slug)
            if check.posted_by == request.user:
                instance = check
                form = EditListingForm(request.POST, instance=instance)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('accounts:mylistings'))
                else:
                    return render(request, 'accounts/editlisting.html', {'exception':True})
            

    else:
        context = {'nologin':'You need to be logged in to do that.'}
        return render(request, 'accounts/editlisting.html', context)


@login_required
def delete_listing(request,slug):
    if request.user.is_authenticated:
        try:
            instance = gamePost.objects.get(slug=slug)
            if instance.posted_by == request.user:
                instance.delete()
                return redirect(reverse('accounts:mylistings'))
            else:
                return render(request, 'accounts/deletelisting.html', {'nopermission':True})
        except:
            return render(request, 'accounts/deletelisting.html', {'exception':True})

