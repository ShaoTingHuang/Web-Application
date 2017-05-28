from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports the Item class
from network.models import *
from network.forms import RegistrationForm, ProForm

from django.core.files import File

import time

@login_required
def home(request):
    all_items = Item.objects.all()
    print all_items
    return render(request, 'network/home.html', {'items': all_items, 'login_user': request.user})

@login_required
def profile(request,user_name):
    context = {}
    look_user = User.objects.get(username = user_name)
    context['look_user'] = look_user
    items = Item.objects.filter(user = look_user)
    context['items'] = items
    profile = Profile.objects.get(user = look_user)
    context['profile'] = profile
    user = request.user
    context['user'] = user
    user_profile = Profile.objects.get(user = user)
    if user_profile in user_profile.Follows.all():
        context['followed'] = 1
    else:
        context['followed'] = 0
    return render(request, 'network/profile.html', context)

@login_required
def add_item(request):
    errors = []
    if 'item' not in request.POST or not request.POST['item']:
        errors.append('You must enter an item to add.')
    else:
        new_item = Item(text=request.POST['item'],
                        user=request.user,
                        time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        )
        new_item.save()

    items = Item.objects.all()
    context = {'items': items, 'errors': errors, 'login_user': request.user}
    return render(request, 'network/home.html', context)

@login_required
def delete_item(request, item_id, user_name):
    errors = []
    context={}
    if request.method != 'POST':
        errors.append('Deletes must be done using the POST method')
    else:
        try:
            item_to_delete = Item.objects.get(id=item_id)
            item_to_delete.delete()
        except ObjectDoesNotExist:
            errors.append('There is no post.')
    look_user = User.objects.get(username = user_name)
    context['look_user'] = look_user
    items = Item.objects.filter(user = look_user)
    context['items'] = items
    profile = Profile.objects.get(user = look_user)
    context['profile'] = profile
    user = request.user
    context['user'] = user
    user_profile = Profile.objects.get(user = user)
    if user_profile in user_profile.Follows.all():
        context['followed'] = 1
    else:
        context['followed'] = 0
    return render(request, 'network/profile.html', context)

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'network/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        print 66
        return render(request, 'network/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        )
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    new_profile = Profile(Lastname=form.cleaned_data['last_name'],
                          Firstname=form.cleaned_data['first_name'],
                          user = new_user,
                          )
    new_profile.save()

    login(request, new_user)
    return redirect(reverse('home'))


def get_photo(request, user_name):
    Users = User.objects.get(username = user_name)
    profile = get_object_or_404(Profile, user=Users)
    return HttpResponse(profile.photo, content_type=profile.content_type)


@login_required
@transaction.atomic
def edit(request):
    context = {}

    if request.method == 'GET':
        profile = Profile.objects.get(user = request.user)
        form = ProForm(instance =profile)
        context['form'] = form
        context['Users'] = request.user
        return render(request,'network/edit.html', context)

    new_profile = Profile.objects.select_for_update().get(user=request.user)
    form = ProForm(request.POST, request.FILES, instance=new_profile)

    if not form.is_valid():
        context['form'] = form
        context['message'] = ['you should upload file']
        return render(request, 'network/edit.html', context)
    else:
        new_profile.content_type = form.cleaned_data['photo'].content_type
        form.save()

        context['message'] = ['Edition saved']
        Users = request.user
        context['Users'] = Users
        items = Item.objects.all()
        context['items']=items
        profile = Profile.objects.get(user = Users)
        context['profile'] = profile
    return render(request, 'network/home.html', context)

def get_photo(request, user_name):
    Users = User.objects.get(username = user_name)
    profile = get_object_or_404(Profile, user=Users)
    return HttpResponse(profile.photo, content_type=profile.content_type)

@login_required
def followstream(request):
    items = Item.objects.all()
    myProfile = Profile.objects.get(user = request.user)
    followlist = myProfile.Follows.all()
    followfinal = []
    for item in items:
        profile = Profile.objects.get(user = item.user)
        if profile in followlist:
            followfinal.append(item)

    context = {'items': followfinal,
               'profile': Profile.objects.get(user = request.user),
               'Users': request.user
               }
    return render(request,'network/followerStream.html',context)

@login_required
def follow(request, user_name):
    look_user = User.objects.get(username = user_name)
    lookProfile = Profile.objects.get(user = look_user)
    myProfile= Profile.objects.get(user = request.user)
    myProfile.Follows.add(lookProfile)
    context = {'items': Item.objects.filter(user = look_user),
               'profile': Profile.objects.get(user = look_user),
               'Users': request.user
               }
    if lookProfile in myProfile.Follows.all():
        context['followed'] = 1
    else:
        context['followed'] = 0
    return render(request,'network/profile.html',context)

@login_required
def unfollow(request, user_name):
    look_user = User.objects.get(username = user_name)
    lookProfile = Profile.objects.get(user = look_user)
    myProfile= Profile.objects.get(user = request.user)
    myProfile.Follows.add(lookProfile)
    context = {'items': Item.objects.filter(user = look_user),
               'profile': Profile.objects.get(user = look_user),
               'Users': request.user
               }
    if lookProfile in myProfile.Follows.all():
        context['followed'] = 0
    else:
        context['followed'] = 1
    return render(request,'network/profile.html',context)
