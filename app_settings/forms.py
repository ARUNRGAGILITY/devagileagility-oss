from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import *

class NewLevelsForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=NewLevels.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)
    help_links = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['parent'] = TreeNodeChoiceField(
            queryset=NewLevels.objects.filter(active=True, author=user),
            label='Select a parent',
            empty_label='--Select parent --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select parent--'


    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent.author != self.user:
            raise forms.ValidationError("You cannot set a parent that belongs to another user.")
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    class Meta:
        model = NewLevels
        fields = ['parent', 'title', 'description', 'help_links', ]


