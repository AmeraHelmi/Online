from django import forms
from myapp.models import *
class UploadFileForm(forms.ModelForm):
    # _myfile = forms.FileField(label='browse file', max_length=100)
    class Meta:
        # Provide an association between the ModelForm and a model
        model = UploadFile
        fields = ['myfile']
