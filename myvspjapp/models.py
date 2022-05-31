from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from taggit.managers import TaggableManager

from enum import Enum


# Create your models here.
class Faculty(models.Model):
    """
    Facultee name: eg. Chair of Technical Studies
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    shortname = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"


class Chair(models.Model):
    """
    Chair name (eg. Computer Science)
    """
    id = models.AutoField(primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    english_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"

    def getShotName(self):
        return f"{self.short_name}"


class Subject(models.Model):
    """
    Subjects (eg. Mathematics 1)
    """
    id = models.AutoField(primary_key=True)
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    language = models.CharField(max_length=30, default='Česky')
    recommended_semester = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    def get_short_name(self):
        return f"{self.short_name}"



def get_path(year, subject, doctype):
    if year == 0:
        year = 'unknown_year'
    subject = Subject.get_short_name(subject)
    print(f"{subject}/{year}/{doctype}/")
    return f"{subject}/{year}/{doctype}/"


class Files(models.Model):

    """
        class Doctype(models.IntegerChoices):
        OTHER = 0, 'Other'
        EXAM = 1, 'Exam'
        LAB = 2, 'Lab'
        HOMEWORK = 3, 'Homework'
    """
    doc_types = {
        0: 'Other',
        1: 'Exam',
        2: 'Lab',
        3: 'Homework',
    }

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    upload_date = models.DateTimeField(default=now)
    is_anonymous = models.BooleanField(default=False)
    description = models.TextField(default="I'm too lazy to write a few words")
    download_count = models.IntegerField(default=0)
    size = models.BigIntegerField(default=0)
    year = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    #tags = models.ManyToManyField("Tag", through="Tagging")
    tags = TaggableManager(blank=True)
    is_verified = models.BooleanField(default=False)
    # doctype = models.IntegerField(default=0)
    # path = get_path(year, subject.id, doc_types.get(doctype))
    # TODO make folder structure based on year, subject and type of document
    url = models.FileField("", upload_to='filevault/')

    def __str__(self):
        return self.url


class FileScore(models.Model):
    """
    file rating model
    """
    file = models.ForeignKey(Files, on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    score = models.FloatField(default=0)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)

