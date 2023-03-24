from django import forms
from .models import Users
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
import datetime
import re
from django.core.exceptions import ValidationError

# widgets are dictionarties which are used to render the form fields in the html template


class Register(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ['Firstname', 'Lastname', 'Email', 'mobile_phone', 'image']
        widgets = {
            'Firstname': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'Lastname': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'Email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'mobile_phone': forms.TextInput(attrs={'placeholder': 'Mobile Phone'}),
        }

    # to describe the behavior of the form and to set the method of the form to POST and add a submit button to the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Create User'))
        self.fields['image'].widget.attrs['enctype'] = 'multipart/form-data'

    # to get the data from the form after the form is validated

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        firstname = cleaned_data.get('Firstname')
        lastname = cleaned_data.get('Lastname')
        email = cleaned_data.get('Email')
        mobile = cleaned_data.get('mobile_phone')
        image = self.cleaned_data.get('image')
        # to make sure all fields are not empty
        if not password1 or not password2 or not firstname or not lastname or not email or not mobile or not image:
            raise forms.ValidationError('Please fill all the fields')

        # if the passwords do not match we raise an error to the user using the ValidationError else we return the cleaned data
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        # to make sure that the image field inputs only images
        if not image.content_type.startswith('image'):
            raise forms.ValidationError('File is not an image')

        return cleaned_data
    # here after the form is validated we return the cleaned data we set the password and the repeat password of the user

    def save(self, commit=True):
        user = super().save(commit=False)
        x = self.cleaned_data.get('password1')
        user.Password = x
        user.RepeatPassword = x
        if commit:
            user.save()
        return user

# the form for login the user by using email and password


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'login-form'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(
            Submit('submit', 'Login', css_class='btn-primary'))

        self.helper.layout = Layout(
            Field('email', css_class='form-control'),
            Field('password', css_class='form-control')
        )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        # if the email and password are empty
        if not email and not password:
            raise forms.ValidationError(
                "Please enter a email and password.")

        elif not email:
            raise forms.ValidationError("Please enter a email.")
        elif not password:
            raise forms.ValidationError("Please enter a password.")
        # if email and password arent empty we return the cleaned data
        return cleaned_data

# form to add the optional info of the user


class OptionalInfoForm(forms.ModelForm):

    BirthDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Users
        fields = ['BirthDate', 'Facebook', 'Country']

    def clean(self):
        cleaned_data = super().clean()
        facebook_url = cleaned_data.get('Facebook')
        birthdate = cleaned_data.get('BirthDate')

        # Validate Facebook URL to make sure that the link provided is a facebook url
        if facebook_url:
            if not re.match(r'^https?://(www\.)?facebook\.com/', facebook_url):
                raise ValidationError('Please enter a valid Facebook URL')

        # Validate BirthDate to make sure the BirthDate  given by the user isnt a date from the future
        if birthdate:
            if birthdate.date() > datetime.date.today():
                raise ValidationError('Birth date cannot be in the future')

# here is the form to edit  info of the user


class UserUpdatedOptionalForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['Firstname', 'Lastname', 'Password',
                  'RepeatPassword', 'mobile_phone', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['enctype'] = 'multipart/form-data'
