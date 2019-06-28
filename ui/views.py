# -*- coding: utf-8 -*-

import datetime
import re
from datetime import timedelta
from typing import Tuple

import reverse_geocoder as rg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from ui.models import Commute, User


def phone_format(phone_number):
    """Remove all non numerical characters."""
    return re.sub('[^0-9]', '', phone_number)


def _process_coordinates(coordinates: str) -> Tuple[float, float]:
    return tuple(
        float(x.strip())
        for x in coordinates.split(',')
    )


WEEKDAYS_NAMES = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

WORKING_DAYS = {0, 1, 2, 3, 4}


@require_GET
def welcome(request):
    """Show the welcome page."""
    return render(request, 'home.html')


@login_required
@require_GET
def new_commute(request):
    return render(request, 'create_commute.html')


@login_required
def user_home(request):
    return render(request, 'user_home.html')


@require_POST
def signup(request):
    first_name = request.POST.get('first')
    last_name = request.POST.get('last')
    email = request.POST.get('email')
    password = request.POST.get('password')
    contact = request.POST.get('contact')

    if not contact:
        contact = '0'

    if None in [first_name, last_name, email, password, contact]:
        return render(request, 'home.html')

    # Check if user exists
    if User.objects.filter(email=email).exists():
        return render(request, 'home.html', context={"user_already_exists": True})

    user = User.objects.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        contact_number=phone_format(contact),
        password=password
    )
    user = authenticate(username=email, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/user_home')
        else:
            return render(request, 'home.html')

    return render(request, 'home.html')


@require_POST
def signin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(username=email, password=password)

    if user is None:
        return render(request, 'home.html', context={"not_registered_user": True})

    if user.is_active:
        login(request, user)
        return HttpResponseRedirect('/user_home')

    else:
        print('what the fuck')


@login_required
@require_POST
def save_commute(request):
    seats = request.POST.get('seats')
    start = request.POST.get('start_destination')
    end = request.POST.get('end_destination')
    time = request.POST.get('dateStart')
    repeat = request.POST.get('repeat')

    if '' in [start, end, time, seats]:
        return render(request, 'user_home.html', context={'successful': False})

    time = datetime.datetime.strptime(time, "%d/%m/%Y %H:%M")

    start_coordinate = start_lat, start_long = _process_coordinates(start)
    end_coordinate = end_lat, end_long = _process_coordinates(end)

    start_res = rg.search(start_coordinate)
    end_res = rg.search(end_coordinate)

    if repeat == 'week':
        for day in range(0, 8):
            extended_time = time + timedelta(days=day)
            _, _ = Commute.objects.get_or_create(
                user=request.user,
                time=extended_time,
                start_latitude=start_lat,
                start_longitude=start_long,
                start_name=start_res[0]['name'] if start_res else None,
                end_latitude=end_lat,
                end_longitude=end_long,
                end_name=end_res[0]['name'] if start_res else None,
                seats=seats,
            )

    elif repeat == '2weeks':
        for day in range(0, 15):
            extended_time = time + timedelta(days=day)
            _, _ = Commute.objects.get_or_create(
                user=request.user,
                time=extended_time,
                start_latitude=start_lat,
                start_longitude=start_long,
                start_name=start_res[0]['name'] if start_res else None,
                end_latitude=end_lat,
                end_longitude=end_long,
                end_name=end_res[0]['name'] if start_res else None,
                seats=seats,
            )

    else:
        _, _ = Commute.objects.get_or_create(
            user=request.user,
            time=time,
            start_latitude=start_lat,
            start_longitude=start_long,
            start_name=start_res[0]['name'] if start_res else None,
            end_latitude=end_lat,
            end_longitude=end_long,
            end_name=end_res[0]['name'] if start_res else None,
            seats=seats,
        )
    return render(request, 'user_home.html', context={'successful': True})


@require_GET
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'home.html')


@require_GET
@login_required
def delete_commutes(request):
    commutes_to_delete = request.GET.getlist('commutes[]')

    for commute_id in commutes_to_delete:
        Commute.objects.filter(user=request.user, id=commute_id).delete()

    user_commutes = Commute.objects.filter(user=request.user)

    # Filter commutes to only working days
    user_commutes = [
        commute
        for commute in user_commutes
        if commute.time.weekday() in WORKING_DAYS
    ]

    return render(
        request, 'my_commutes.html',
        context={"commutes": user_commutes, "WEEKDAYS": WEEKDAYS_NAMES}
    )


@require_GET
@login_required
def search_commute(request):
    """Display the commute board."""
    now = datetime.datetime.now()
    commutes = Commute.objects.filter(
        time__gte=now,
        time__lte=now + timedelta(days=7)
    ).order_by('time')

    # Filter commutes to only working days
    # Sort commutes by date so only the most recent commute is rendered in the map

    commutes = [
        commute
        for commute in commutes
        if commute.time.weekday() in WORKING_DAYS
    ]

    return render(
        request, 'search_commute.html',
        context={"commutes": commutes, "now": now, "WEEKDAYS": WEEKDAYS_NAMES}
    )


@require_GET
@login_required
def my_commutes(request):
    user_commutes = Commute.objects.filter(user=request.user)

    return render(request, 'my_commutes.html', context={"commutes": user_commutes, "WEEKDAYS": WEEKDAYS_NAMES})
