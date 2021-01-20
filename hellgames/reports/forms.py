from django.forms import ModelForm
from .models import Report
from user.models import CustomUser
from django import forms


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['post_title', 'post_text', 'posted_by']
    
    def __init__(self, *args, **kwargs):
        user_from = kwargs.pop('user_from')
        super(ReportForm, self).__init__(*args, **kwargs)
        # fix user_to email to username // NOT SECURE enough.
        self.fields['posted_by'] = forms.ModelChoiceField(queryset=CustomUser.objects.filter(username=user_from))
        
        self.fields['posted_by'].label = "Verify your e-mail:"

        self.fields['post_title'].widget.attrs['class'] = 'form-control'
        self.fields['post_text'].widget.attrs['class'] = 'form-control'
        self.fields['posted_by'].widget.attrs['class'] = 'form-control'