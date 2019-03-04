from django import forms


class NoteForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(label='Note', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
