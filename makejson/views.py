import os.path

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from myvspjapp.models import Subject, Files
from django.core import serializers
import os
import pathlib
import json

# Create your views here.


@csrf_exempt
def make_json(request):
    subjects = Subject.objects.all()

    # return JsonResponse({"Output": "Capital API"})
    return JsonResponse(list(Subject.objects.all().values()), safe=False)


def test_json(request):
    json_result = []

    # for subject in Subject.objects.all():
    #     subjects = []  # top level nodes, subjects list
    #     json_result.append({
    #         'text': subject.short_name,
    #         'icon': 'fa-solid fa-folder'
    #     })
    #     s_id = subject.id
    #     years = get_years_list(s_id)
    #     print(f"- {subject}")
    #     for year in years:
    #         print(f"- - {year}")
    #         for file in Files.objects.filter(subject_id=subject.id, year=year):
    #             print(f"- - -{file.url}")
    # #return json.dumps(json_result)
    return JsonResponse(json_result, safe=False, json_dumps_params={'ensure_ascii':False})
    #return HttpResponse(json_result)


def get_years_list(s_id):
    """
    #TODO change method not to iterate all subjects. Can be solved by adding distinct, but with another db engine?
    :param s_id: subject id
    :return: list of strings
    """
    result = []
    for file in Files.objects.filter(subject_id=s_id).order_by('-year'):
        if file.year not in result:
            result.append(file.year)

    return result


def get_filename(url):
    return os.path.basename(url)


def get_icon(filename):
    ext = pathlib.Path(filename).suffix
    pass
