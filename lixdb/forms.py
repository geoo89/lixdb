from django import forms
# from rango.models import Replay
from lixdb.models import UserProfile
from django.contrib.auth.models import User

# class ReplayForm(forms.ModelForm):
#     name = forms.CharField(max_length=128, widget=forms.FileInput(), help_text="Please enter the file path.")

#     class Meta:
#         model = Category
#         fields = ('name')

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    upfile = forms.FileField(label = 'Select a file')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = UserProfile
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ()

# class FileForm(forms.Form):
#     