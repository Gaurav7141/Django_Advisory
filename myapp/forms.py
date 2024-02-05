# yourappname/forms.py
from django import forms
from .models import EmailCredentials



class EmailCredentialsForm(forms.ModelForm):
    class Meta:
        model = EmailCredentials
        fields = ['tenant', 'to', 'cc', 'subject', 'url', 'api_key']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add a common class to all text input fields
        for field_name in self.fields:
            if isinstance(self.fields[field_name].widget, forms.TextInput):
                self.fields[field_name].widget.attrs['class'] = 'common-input'

class SearchCredentialsForm(forms.Form):
    tenant = forms.CharField(label='Search by Tenant', max_length=255)


class UserInputForm(forms.Form):
    ADVISORY_CHOICES = [
        ('M', 'Malware'),     ('V', 'Vulnerability'),
    ]

    advisory_type = forms.ChoiceField(
        choices=ADVISORY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'advisory-type-radio'}),
    )

    advisory_number = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter Advisory Number', 'class': 'input-box'})
    )

    advisory_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Advisory Name', 'class': 'input-box'})
    )

    # advisory_file_name = forms.FileField(
    #     label='Advisory File',
    #     help_text='max. 5 MB',
    #     widget=forms.ClearableFileInput(attrs={'class': 'input-box'}),
    # )
    # advisory_file_name = forms.CharField(
    # label='Advisory File',
    # help_text='max. 5 MB',
    # widget=forms.TextInput(attrs={'class': 'input-box'}),
    # )   

    advisory_file = forms.FileField(
        label='Advisory File',
        help_text='max. 5 MB',
        # widget=forms.ClearableFileInput(attrs={'class': 'input-box'}),
        widget=forms.ClearableFileInput(attrs={'class': 'input-box', 'accept': '.htm'}),
    )