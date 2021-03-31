from django import forms

from .models import Subscribers


class Subscribe(forms.Form):
    Email = forms.EmailField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'padding: 5px;',
                'placeholder': 'Enter email'
            }
        ))

    def clean_Email(self):
        cleaned_email = self.cleaned_data.get('Email')
        if (cleaned_email == ''):
            raise forms.ValidationError('This field cannot be blank')

        for subscriber in Subscribers.objects.all():
            if subscriber.email == cleaned_email \
                 and subscriber.confirmed is False:
                raise forms.ValidationError('This email already exists, but is not confirmed. \
                    Please check your email to confirm your email address.')
            if subscriber.email == cleaned_email:
                raise forms.ValidationError('This email already exists.')
        return cleaned_email

    def __str__(self):
        return self.Email
