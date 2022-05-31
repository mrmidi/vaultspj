import sys

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from myvspjapp.models import Subject, Files
import os
import json

# Create your views here.
import makejson.views
# TODO make some kind of cache system, load static JSON if no new files was uploaded


def get_files_list(s_id, year):
    result = []
    for file in Files.objects.filter(subject_id=s_id, year=year):
        result.append({
            'text': get_filename(str(file.url)),
            'icon': 'fa-solid fa-file'
        })
    return result


def get_years_list(s_id):
    """
    #TODO change method not to iterate all subjects. Can be solved by adding distinct, but with another db engine?
    :param s_id: subject id
    :return: list of strings
    """
    result = []
    years = []
    for file in Files.objects.filter(subject_id=s_id).order_by('-year'):
        if file.year not in years:
            years.append(file.year)
            y = file.year
            if y == 0:
                y = 'Unknown'
            result.append({
                'text': y,
                'icon': 'fa-solid fa-folder',
                'nodes': get_files_list(s_id, file.year)
            })
    return result


def get_subjects(semester):
    json_result = []
    for subject in Subject.objects.filter(recommended_semester=semester).order_by('name'):
        s_id = subject.id
        if Files.objects.filter(subject_id=s_id).values('year').count() > 0:
            json_result.append({
                'text': f'{subject.name}',
                'icon': 'fa-solid fa-folder',
                'nodes':
                    get_years_list(s_id)
            })
        else:
            json_result.append({
                'text': f'{subject.name}',
                'icon': 'fa-solid fa-folder',
            })

    return json_result


def test_json(request):
    json_result = []
    semesters = [1, 2, 3, 4, 5, 6]
    for semester in semesters:
        semesters = []
        json_result.append({
            'text': f'Recommended semester: {semester}',
            'icon': 'fa-solid fa-folder',
            'nodes':
                get_subjects(semester)
        })
        # for subject in Subject.objects.filter(recommended_semester=semester):
        #     json_result.append({
        #         'nodes': [
        #             {
        #                 'text': f'{subject.name}',
        #                 'icon': 'fa-solid fa-folder',
        #             }
        #         ]
        #     })
            # s_id = subject.id
            # years = get_years_list(s_id)
            # print(f"- {subject}")
            # for year in years:
            #     print(f"- - {year}")
            #     for file in Files.objects.filter(subject_id=subject.id, year=year):
            #         print(f"- - -{file.url}")
    return json.dumps(json_result)
    # return JsonResponse(json_result, safe=False, json_dumps_params={'ensure_ascii':False})
    # return json_result





def get_filename(url):
    return os.path.basename(url)


@login_required
def treasureView(request):
    return HttpResponse("Here will be treasures!");


@login_required
def treasure_view(request):
    # json_string = json.dumps(test_json(request), ensure_ascii=False)
    # json_string = test_json(request)
    json_string = json.loads(json.dumps(test_json(request), ensure_ascii=False))

    context = {
        'tree': json_string,
        'other': 'fuck hell',
    }
    print(context)
    return render(request, 'treasurevault/treasurevault.html', context)
