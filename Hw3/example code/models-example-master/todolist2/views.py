from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports the Item class
from todolist2.models import *


# Action for the default /todolist2/ route.
@login_required
def home(request):
    # Gets a list of all the items in the todo-list database.
    all_items = Item.objects.all()
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view.
    return render(request, 'todolist2/index.html', {'items': all_items})


# Action for the /todolist2/add-item route.
@login_required
def add_item(request):
    errors = []  # A list to record messages for any errors we encounter.

    # Adds the new item to the database if the request parameter is present
    if 'item' not in request.POST or not request.POST['item']:
        errors.append('You must enter an item to add.')
    else:
        new_item = Item(text=request.POST['item'],
                        user=request.user,
                        ip_addr=request.META['REMOTE_ADDR'])
        new_item.save()

    # Sets up data needed to generate the view, and generates the view
    items = Item.objects.all()
    context = {'items': items, 'errors': errors}
    return render(request, 'todolist2/index.html', context)


# Action for the /todolist2/delete-item route.
@login_required
def delete_item(request, item_id):
    errors = []

    if request.method != 'POST':
        errors.append('Deletes must be done using the POST method')
    else:
        # Deletes the item if present in the todo-list database.
        try:
            item_to_delete = Item.objects.get(id=item_id)
            item_to_delete.delete()
        except ObjectDoesNotExist:
            errors.append('The item did not exist in the To Do List.')

    items = Item.objects.all()
    context = {'items': items, 'errors': errors}
    return render(request, 'todolist2/index.html', context)

@transaction.atomic
def register(request):
    context = {}
    errors = []
    context['errors'] = errors

    # Just display the registration form if this is a GET request
    if request.method == 'GET':
        return render(request, 'todolist2/register.html', context)

    # Check the validity of the form data
    if not 'username' in request.POST or not request.POST['username']:
        errors.append('Username is required.')
    else:
        # Save the username in the request context to re-fill the username
        # field in case the form has errrors
        context['username'] = request.POST['username']

    if not 'password1' in request.POST or not request.POST['password1']:
        errors.append('Password is required.')
    if not 'password2' in request.POST or not request.POST['password2']:
        errors.append('Confirm password is required.')

    if errors:
        # Required fields are missing.  Display errors, now.
        return render(request, 'todolist2/register.html', context)

    if request.POST['password1'] != request.POST['password2']:
        errors.append('Passwords did not match.')

    if User.objects.select_for_update().filter(username = request.POST['username']).exists():
        errors.append('Username is already taken.')

    if errors:
        # Required fields are missing.  Display errors, now.
        return render(request, 'todolist2/register.html', context)

    # Creates the new user from the valid form data
    new_user = User.objects.create_user(username=request.POST['username'],
                                        password=request.POST['password1'])
    new_user.save()

    # Logs in the new user and redirects to his/her todo list
    new_user = authenticate(username=request.POST['username'],
                            password=request.POST['password1'])
    
    login(request, new_user)
    return redirect('/todolist2/')
