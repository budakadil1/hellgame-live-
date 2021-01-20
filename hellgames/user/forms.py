from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from user.models import CustomUser, Reviews, Profile
from phonenumber_field.formfields import PhoneNumberField

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=60, required=True)
    username = forms.CharField(max_length=24, required=True)
    phone_number = PhoneNumberField()
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        try:
            exists = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already in use.')

    def clean_username(self):
        # Get the username
        username = self.cleaned_data.get('username')
        # check if any users already exist with this username.
        try:
            exists = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username

        raise forms.ValidationError('This username is already in use.')

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2", 'phone_number')
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Password (again)"

        # change help text because default is ugly :D
        self.fields['password1'].help_text = "Choose a password that's longer than 8 characters. Note: Your password can't include anything related to your username/email in it."
        self.fields['password2'].help_text = "Enter your password again."
        self.fields['phone_number'].help_text = "Your phone number will be verified."



        # widgets for form styling 
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class LeaveReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['review_title', 'review_text', 'review_type','review_to', 'review_from']
    
    def __init__(self, *args, **kwargs):
        user_to = kwargs.pop('user_to','')
        user_from = kwargs.pop('contextuser')
        super(LeaveReviewForm, self).__init__(*args, **kwargs)
        # fix user_to email to username // NOT SECURE enough.
        self.fields['review_to'] = forms.ModelChoiceField(queryset=CustomUser.objects.filter(username=user_to))
        self.fields['review_from'] = forms.ModelChoiceField(queryset=CustomUser.objects.filter(username=user_from))

        self.fields['review_title'].widget.attrs['class'] = 'form-control'
        self.fields['review_text'].widget.attrs['class'] = 'form-control'
        self.fields['review_type'].widget.attrs['class'] = 'form-control'
        self.fields['review_to'].widget.attrs['class'] = 'form-control'
        self.fields['review_from'].widget.attrs['class'] = 'form-control'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_description']
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['user_description'] = forms.CharField(required=False, widget=forms.Textarea)
        self.fields['user_description'].label = 'New Description: '
        self.fields['user_description'].widget.attrs['class'] = 'form-control'

class UserMerchantOnlyForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['merchant_status']

    def __init__(self, *args, **kwargs):
        ms_status = kwargs.pop('ms_kw', None)
        super(UserMerchantOnlyForm, self).__init__(*args, **kwargs)
        self.fields['merchant_status'] = forms.BooleanField(required=False, initial=ms_status)
        self.fields['merchant_status'].widget.attrs['class'] = 'generic-checkbox'
        self.fields['merchant_status'].label = "Merchant: "
        
