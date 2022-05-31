from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from myvspjapp.models import Subject, Files
from datetime import date
from django.core.files.storage import FileSystemStorage
from .forms import FileForm
import os

from django import forms
"""
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
"""



# Create your views here.
@login_required
def upload_view(request):
    if (request.method == 'POST'):
        #uploaded_file = request.POST['url']
        print(request.POST)
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            #file.size = uploaded_file.size
            if not request.POST['year'] == 'Unknown':  # if year is unknown - year is 0
                file.year = request.POST['year']
            else:
                file.year = 0
            file.save()
            lastfile = file.url  # get file size
            path = "media/" + str(lastfile)
            size = os.path.getsize(path)
            file.size = size
            file.save()
            form.save_m2m()
            return redirect()
        HttpResponse("file uploaded")
    else:
        form = FileForm()
    context = {
        'form': form,
        'yearlist': populateYears(),
    }
    return render(request, 'upload/upload.html', context)

@login_required
def uploadView(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            print("* * * FORM DATA")
            print(form.cleaned_data)
            print("* * *")
        current_user = request.user
        print(request.POST)
        file = Files()  # create and fill file object
        file.subject_id = request.POST['subject']
        file.year = request.POST['year']
        file.tags = request.POST['tags']
        if request.POST['description']:
            file.description = request.POST['description']

        if request.POST['anonymous']:
            file.is_anonymous = True
        if request.POST['noyear']:
            file.year = 0
        file.user_id = current_user.id
        #file.subject_id = request.POST['']

        uploaded_file = request.FILES['file']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        saved = fs.save(uploaded_file.name, uploaded_file)
        file.url = fs.url(saved)
        print(file.url)
        #file.save()
        #file.save(commit=True)
        #file.save()

        #name = fs.save(uploaded_file.name, uploaded_file)
        #url = fs.url(name)
        # S A V E

        # S A V E


        return HttpResponse("File uploaded!")
    else:
        subjects = Subject.objects.order_by('recommended_semester', 'name')
        yearlist = populateYears()
        context = {'subjects': subjects,
                   'yearlist': yearlist,
                   }
        return render(request, 'upload/upload.html', context)

def populateYears():
    """
    function creates list of years starting from current year
    and down to 2010. used by upload form to display years
    function is used for not changing list every year
    :return:
    """
    year = date.today().year
    yearslist = []
    while year >= 2010:
        yearslist.append(year)
        year -= 1
    yearslist.append('Unknown')
    return yearslist

def processTags(tags, file_id):
    taglist = tags.split(',')
    for tag in taglist:
        tag = tag.strip()
        tag = Tag.objects.get_or_create(tag=tag.lower())
        if tag.id:
            tagging = Tagging.objects.get_or_create(files_id=file_id)

