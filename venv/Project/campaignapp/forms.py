from django.core.validators import MaxValueValidator, MinValueValidator
from .models import Rating
from django import forms
from .models import Campaign, Picture, Tag, ProjectComment, User_Donation, Rating,Category
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.forms import ClearableFileInput, ModelMultipleChoiceField
import imghdr

# class built in to make the user able to select multiple files with a choice to remove them





class AddNewProduct(forms.ModelForm):
    pictures = forms.ImageField( widget=forms.ClearableFileInput(attrs={'multiple': True,'accept':'image/*'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Campaign
        fields = ['title', 'details', 'category', 'pictures','total_target', 'tags', 'start_time', 'end_time', 'donation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        title=cleaned_data.get('title')
        details=cleaned_data.get('details')
        category=cleaned_data.get('category')
        total_target=cleaned_data.get('total_target')

        if not start_time or not end_time or not total_target or not details or not category  or not title:
            raise forms.ValidationError('Please fill all fields ')
        if Campaign.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError('Campaign with this name already exists')
        # to make sure that the start time is before the end time
        if end_time and start_time and end_time < start_time:
            raise ValidationError('End time cannot be before start time.')


#added the same class as AddProject but without title validation
class EditProduct(forms.ModelForm):
    pictures = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True,'accept':'image/*'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Campaign
        fields = ['title', 'details', 'category', 'pictures','total_target', 'tags', 'start_time', 'end_time', 'donation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        title=cleaned_data.get('title')
        details=cleaned_data.get('details')
        category=cleaned_data.get('category')
        total_target=cleaned_data.get('total_target')

        if not start_time or not end_time or not total_target or not details or not category  or not title:
            raise forms.ValidationError('Please fill all fields ')
        # to make sure that the start time is before the end time
        if end_time and start_time and end_time < start_time:
            raise ValidationError('End time cannot be before start time.')

class CommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ['comment_text']



class DonationForm(forms.ModelForm):
    class Meta:
        model = User_Donation
        fields = ['donate']



class PictureForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Campaign
        fields = ['pictures']


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['rating']
    # to limit the user to 5 ratings and not less than 1

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if not rating:
            raise forms.ValidationError('Please select a rating')
        if not 1 <= rating <= 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

    def clean_name(self):
        name = self.cleaned_data['name']
        #here we check if the tag already exists regardless the previous category is in uppercase or lowercase
        if not name:
            raise forms.ValidationError('Enter a Category name')

        if Category.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('This category already exists')
        return name
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    def __init__(self, *args, **kwargs):

        super(TagForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('Please enter a valid  Tag name')
        #here we check if the tag already exists regardless the previous tag is in uppercase or lowercase
        if Tag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError('This Tag already exists')
        return name
    