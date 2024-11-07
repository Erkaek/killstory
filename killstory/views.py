"""
Views for the killstory application.

These views handle the rendering of pages related to killmails, victims, attackers, and associated items.

The views require the user to be logged in to access them, as enforced by the `@login_required` decorator.
"""

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Killmail, Victim, VictimItem, VictimContainedItem, Attacker

@login_required
def killstory_view(request):
    """
    View function that renders the index page for the killstory application.

    This view retrieves all Killmail objects from the database and passes them to the template
    'killstory/index.html' to be displayed on the index page.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The rendered response for the index page with the Killmail objects.
    """
    kill_killmails = Killmail.objects.all()
    context = {
        'kill_killmails': kill_killmails
    }
    return render(request, 'killstory/index.html', context)

@login_required
def kill_detail_view(request, killmail_id):
    """
    View function that renders the detail page for a specific killmail.

    This view retrieves the Killmail object corresponding to the provided killmail_id and passes it to the template
    'killstory/kill_detail.html' to be displayed on the killmail detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        killmail_id (int): The primary key ID of the Killmail object to retrieve.

    Returns:
        HttpResponse: The rendered response for the killmail detail page.
    """
    killmail = get_object_or_404(Killmail, pk=killmail_id)
    context = {
        'killmail': killmail
    }
    return render(request, 'killstory/kill_detail.html', context)

@login_required
def victim_detail_view(request, victim_id):
    """
    View to display the details of a specific Victim.

    This view retrieves a Victim object based on the provided ID (victim_id).
    It requires the user to be authenticated in order to access the details.
    If the Victim object does not exist, a 404 error is raised.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        victim_id (int): The ID of the Victim to retrieve.

    Returns:
        HttpResponse: The rendered 'victim_detail.html' template with the Victim context.
    """
    victim = get_object_or_404(Victim, pk=victim_id)
    context = {
        'victim': victim
    }
    return render(request, 'killstory/victim_detail.html', context)

@login_required
def attacker_detail_view(request, attacker_id):
    """
    View to display the details of a specific Attacker.

    This view retrieves an Attacker object based on the provided ID (attacker_id).
    It requires the user to be authenticated in order to access the details.
    If the Attacker object does not exist, a 404 error is raised.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        attacker_id (int): The ID of the Attacker to retrieve.

    Returns:
        HttpResponse: The rendered 'attacker_detail.html' template with the Attacker context.
    """
    attacker = get_object_or_404(Attacker, pk=attacker_id)
    context = {
        'attacker': attacker
    }
    return render(request, 'killstory/attacker_detail.html', context)

@login_required
def victim_item_detail_view(request, item_id):
    """
    View to display the details of a specific VictimItem.

    This view retrieves a VictimItem object based on the provided ID (item_id).
    It requires the user to be authenticated in order to access the details.
    If the VictimItem object does not exist, a 404 error is raised.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        item_id (int): The ID of the VictimItem to retrieve.

    Returns:
        HttpResponse: The rendered 'victim_item_detail.html' template with the VictimItem context.
    """
    item = get_object_or_404(VictimItem, pk=item_id)
    context = {
        'item': item
    }
    return render(request, 'killstory/victim_item_detail.html', context)

@login_required
def victim_contained_item_detail_view(request, contained_item_id):
    """
    View to display the details of a specific VictimContainedItem.

    This view retrieves a VictimContainedItem object based on the provided ID (contained_item_id).
    It requires the user to be authenticated in order to access the details.
    If the VictimContainedItem object does not exist, a 404 error is raised.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        contained_item_id (int): The ID of the VictimContainedItem to retrieve.

    Returns:
        HttpResponse: The rendered 'victim_contained_item_detail.html' template with the VictimContainedItem context.
    """
    contained_item = get_object_or_404(VictimContainedItem, pk=contained_item_id)
    context = {
        'contained_item': contained_item
    }
    return render(request, 'killstory/victim_contained_item_detail.html', context)
