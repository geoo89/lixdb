from django.shortcuts import render
from django.http import HttpResponse

from django.template import RequestContext
from django.shortcuts import render_to_response

from lixdb.models import Directory, Level, Replay

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
    return HttpResponse("This is the about page! <a href=\"../\">Back</a> <a href=\"/lixdb/\">Home</a>")

def level_list(request, root_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    #directory_name = directory_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'root_name': root_name_url}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        directory = Directory.objects.get(name=root_name_url)
        context_dict['directory'] = directory

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        levels = Level.objects.filter(parent = directory)
        directories = Directory.objects.filter(parent = directory)

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