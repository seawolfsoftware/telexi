from django import forms


class Notify(forms.Form):
    Email = forms.EmailField()

    def __str__(self):
        return self.Email
