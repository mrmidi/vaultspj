from datetime import date

from crispy_forms.helper import FormHelper
from django import forms
from myvspjapp.models import Subject

from myvspjapp.models import Files


def populateYears():
    """
delete it
    :return:
    """
    year = date.today().year
    yearslist = []
    while year >= 2010:
        yearslist.append(year)
        year -= 1
    #return dict(zip(yearslist, yearslist))
    return yearslist


class FileForm(forms.ModelForm):
    subject = forms.ModelChoiceField(Subject.objects.order_by('recommended_semester', 'name'), empty_label=None)
    #tags = forms.CharField(blank=True)
    class Meta:
        model = Files
        fields = ('url', 'is_anonymous', 'subject', 'description', 'tags')

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

