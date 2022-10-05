from django import forms




class Search(forms.Form):
    search = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder' : 'Search items',
        'type' : 'search',
        'class' : 'form-control me-2',
        'name' : 'search'
    }))