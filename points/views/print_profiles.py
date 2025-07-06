from django.shortcuts import render #type: ignore
from points.models import Camper #type: ignore
from points.utils import create_profile #type: ignore
from points.wrappers import admin_only #type: ignore


@admin_only
def print_profiles(request):
    program = request.user.program
    if request.method == 'GET':
        campers = {}
        all = Camper.objects.filter(program=program).order_by('new_bunk__number', 'last_name')
        for camper in all:
            campers[camper] = create_profile(camper)

        return render(request, 'points/print_profiles.html', {
            'campers': campers,
        })