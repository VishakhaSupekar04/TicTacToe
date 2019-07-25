from django.forms import ModelForm

from .models import Invitation

#this class creates a invitation html form by taking the models.py class Invitation
#It also takes care of the validation of data
#hence we donnot have to create a HTML form . Django provides that for us


class InvitationForm(ModelForm):
    class Meta:
        model =Invitation
        exclude = ('from_user','timestamp')  # we don't want these fields to show on the form