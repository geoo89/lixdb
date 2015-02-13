from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from lixdb.models import Directory, Level, Replay
from lixdb.forms import UserForm, UserProfileForm

import os


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    directories = Directory.objects.order_by('name')
    levels = Level.objects.order_by('name')

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'directories': directories, 'levels': levels}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('lixdb/index.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    context_dict = dict()

    return render_to_response('lixdb/about.html', context_dict, context)


def level_list(request, root_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    #directory_name = directory_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'root_name': root_name_url, 'parent_dir': os.path.join(root_name_url, '..')}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        directory = Directory.objects.get(name=root_name_url)
        context_dict['directory'] = directory

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        levels = Level.objects.filter(parent = directory).order_by('oid')
        directories = Directory.objects.filter(parent = directory).order_by('oid')

        level_stats = []
        for level in levels:
            stats = [0, 0, 999999, 999999] # turn this into a class?
            success = False
            rpls = Replay.objects.filter(level_path = level.name)
            for r in rpls:
                stats = [max(stats[0], r.lems_saved), r.lems_required, min(stats[2], r.skills), min(stats[3], r.time)]
                if r.status == '(OK)':
                    success = True
            if success:
                level_stats.append([level, stats])
            else:
                level_stats.append([level])

        # Adds our results list to the template context under name pages.
        context_dict['level_stats'] = level_stats
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['directories'] = directories
    except Directory.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('lixdb/levels.html', context_dict, context)


def replay_list(request, root_name_url):
    context = RequestContext(request)

    level = Level.objects.get(name=root_name_url)
    replays = Replay.objects.filter(level_path = root_name_url)
    replays_by_saved = replays.order_by('-lems_saved', 'skills')
    replays_by_skills = replays.order_by('skills', '-lems_saved')
    replays_by_time = replays.order_by('time')

    context_dict = {'level_name': root_name_url, 'dir_name': level.parent.name}
    context_dict['replays_by_saved'] = replays_by_saved
    context_dict['replays_by_skills'] = replays_by_skills
    context_dict['replays_by_time'] = replays_by_time

    return render_to_response('lixdb/replays.html', context_dict, context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # # Did the user provide a profile picture?
            # # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
            #     profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'lixdb/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/lixdb/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Lix DB account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('lixdb/login.html', {}, context)


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/lixdb/')