from django import forms
from django.forms import ModelForm
from .models import gamePost, gameIdentifier
from user.models import CustomUser

class ListingForm(ModelForm):
    class Meta:
        model = gamePost
        fields = ['post_title', 'post_text', 'post_category', 'price', 'posted_by', 'quantity']
    
    post_title = forms.CharField(max_length=32, required=True)
    post_text = forms.CharField(max_length=500, required=False, widget=forms.Textarea)
    post_category = forms.ModelChoiceField(gameIdentifier.objects.all(), required=True)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['posted_by'] = forms.ModelChoiceField(queryset=CustomUser.objects.filter(username=user))
        # add form control as a class so that they are better looking.
        self.fields['posted_by'].widget.attrs['class'] = 'form-control'
        self.fields['post_title'].widget.attrs['class'] = 'form-control'
        self.fields['post_text'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['post_category'].widget.attrs['class'] = 'form-control'
        self.fields['quantity'].widget.attrs['class'] = 'form-control'
        
        # define helptexts.
        self.fields['price'].help_text = "All prices are in USD$."
        self.fields['posted_by'].help_text = "Verify that this is your email."
        self.fields['quantity'].help_text = "Please click this button if you have a large stock of this item and you wish to sell multiple quantities."


        #define emptyarea for dropdown select options. because default ----- looks bad.
        self.fields['post_category'].empty_label = "- CHOOSE A CATEGORY -"
        
        #define better labels for post_title, text and posted_by
        self.fields['post_title'].label = "Listing Title"
        self.fields['post_text'].label = "Listing Description"
        self.fields['posted_by'].label = "E-mail Verification"
        self.fields['quantity'].label = "Multiple Quantities"

        
class EditListingForm(ModelForm):
    class Meta:
        model = gamePost
        fields = ['post_title', 'post_text', 'price']
        post_title = forms.CharField(max_length=32, required=True)
        post_text = forms.CharField(max_length=500, required=False, widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):
        super(EditListingForm, self).__init__(*args, **kwargs)
        self.fields['post_title'].widget.attrs['class'] = 'form-control'
        self.fields['post_text'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'

        
    
