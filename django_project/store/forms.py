from django import forms


class Notify(forms.Form):

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'type': 'email',
               'placeholder': ('Enter email')}))

    def __str__(self):
        return self.email
